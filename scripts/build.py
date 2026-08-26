#!/usr/bin/env python3
"""Aggregate, validate, rank, and publish public BitTorrent tracker lists."""

from __future__ import annotations

import argparse
import base64
import concurrent.futures
import csv
import hashlib
import ipaddress
import json
import os
import re
import secrets
import socket
import ssl
import struct
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILE = ROOT / "sources.json"
DATA_DIR = ROOT / "data"
LIST_DIR = ROOT / "lists"
USER_AGENT = "transmission-global-trackers/1.0 (+https://github.com/cyriusweng/transmission-global-trackers)"
CONTROL_INFOHASH = bytes.fromhex("DAFC8C076CA2F3ED376EEAE7C76A0D6BE2415C45")
TRACKER_RE = re.compile(r"(?i)\b(?:udp|https?|wss?)://[^\s<>\"'`]+")
SUPPORTED_SCHEMES = {"udp", "http", "https", "ws", "wss"}
TRANSMISSION_SCHEMES = {"udp", "http", "https"}
WEBSOCKET_SCHEMES = {"ws", "wss"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value or "source"


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(text, encoding="utf-8")
    temp.replace(path)


def write_lines(path: Path, values: list[str], blank_between: bool = False) -> None:
    separator = "\n\n" if blank_between else "\n"
    atomic_write(path, separator.join(values) + ("\n" if values else ""))


def fetch_text(url: str, timeout: float = 30.0) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read(8 * 1024 * 1024).decode("utf-8", "replace")


def normalise_url(raw: str) -> str | None:
    raw = raw.strip().strip("[](){}<>,;\"'")
    raw = raw.rstrip(".")
    try:
        parsed = urllib.parse.urlsplit(raw)
    except ValueError:
        return None
    scheme = parsed.scheme.lower()
    if scheme not in SUPPORTED_SCHEMES or not parsed.hostname:
        return None
    try:
        port = parsed.port
    except ValueError:
        return None
    host = parsed.hostname.lower().rstrip(".")
    if host in {"localhost", "localhost.localdomain"}:
        return None
    try:
        address = ipaddress.ip_address(host)
        if not address.is_global:
            return None
        host_display = f"[{host}]" if address.version == 6 else host
    except ValueError:
        try:
            host_display = host.encode("idna").decode("ascii")
        except UnicodeError:
            return None
    default_port = {"http": 80, "https": 443, "ws": 80, "wss": 443}.get(scheme)
    if scheme == "udp" and port is None:
        return None
    netloc = host_display
    if port is not None and port != default_port:
        netloc += f":{port}"
    path = parsed.path or "/announce"
    path = re.sub(r"/{2,}", "/", path)
    return urllib.parse.urlunsplit((scheme, netloc, path, parsed.query, ""))


def extract_urls(text: str) -> list[str]:
    found: set[str] = set()
    for match in TRACKER_RE.finditer(text):
        value = normalise_url(match.group(0))
        if value:
            found.add(value)
    return sorted(found)


def address_family_name(family: int) -> str:
    return "ipv6" if family == socket.AF_INET6 else "ipv4"


def resolve_addresses(host: str, port: int, socktype: int) -> list[tuple[int, int, int, tuple[Any, ...]]]:
    addresses: list[tuple[int, int, int, tuple[Any, ...]]] = []
    seen: set[tuple[int, tuple[Any, ...]]] = set()
    for family, kind, proto, _, sockaddr in socket.getaddrinfo(host, port, type=socktype):
        key = (family, sockaddr)
        if key not in seen:
            seen.add(key)
            addresses.append((family, kind, proto, sockaddr))
    return addresses


def validate_udp(parsed: urllib.parse.SplitResult, timeout: float) -> dict[str, Any]:
    port = parsed.port
    if port is None:
        raise ValueError("UDP tracker has no port")
    last_error: Exception | None = None
    for family, kind, proto, sockaddr in resolve_addresses(parsed.hostname or "", port, socket.SOCK_DGRAM):
        sock = socket.socket(family, kind, proto)
        sock.settimeout(timeout)
        started = time.monotonic()
        try:
            transaction_id = secrets.randbits(32)
            request = struct.pack("!QII", 0x41727101980, 0, transaction_id)
            sock.sendto(request, sockaddr)
            response, _ = sock.recvfrom(2048)
            if len(response) < 16:
                raise ValueError("short BEP 15 connect response")
            action, returned_id, _ = struct.unpack("!IIQ", response[:16])
            if action != 0 or returned_id != transaction_id:
                raise ValueError("invalid BEP 15 connect response")
            return {
                "status": "alive",
                "latency_ms": round((time.monotonic() - started) * 1000, 1),
                "ip_version": address_family_name(family),
                "detail": "BEP 15 connect response",
            }
        except Exception as error:  # noqa: BLE001 - every endpoint failure is data
            last_error = error
        finally:
            sock.close()
    raise last_error or RuntimeError("DNS returned no addresses")


def looks_bencoded(data: bytes) -> bool:
    data = data.lstrip()
    return bool(data) and (data[:1] in {b"d", b"l", b"i"} or data[:1].isdigit())


def tracker_probe_urls(parsed: urllib.parse.SplitResult) -> list[str]:
    path = parsed.path or "/announce"
    query_hash = urllib.parse.quote_from_bytes(CONTROL_INFOHASH)
    probes: list[str] = []
    if "announce" in path:
        scrape_path = path.rsplit("announce", 1)[0] + "scrape" + path.rsplit("announce", 1)[1]
        probes.append(urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, scrape_path, f"info_hash={query_hash}", "")))
    separator = "&" if parsed.query else ""
    announce_query = f"{parsed.query}{separator}info_hash={query_hash}"
    probes.append(urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, path, announce_query, "")))
    return probes


def validate_http(parsed: urllib.parse.SplitResult, timeout: float) -> dict[str, Any]:
    last_error: Exception | None = None
    for probe in tracker_probe_urls(parsed):
        started = time.monotonic()
        request = urllib.request.Request(probe, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = response.read(1024 * 1024)
                content_type = response.headers.get("Content-Type", "")
                if looks_bencoded(body) or "bencode" in content_type or "bittorrent" in content_type:
                    return {
                        "status": "alive",
                        "latency_ms": round((time.monotonic() - started) * 1000, 1),
                        "ip_version": "unknown",
                        "detail": f"HTTP {response.status} tracker response",
                    }
                last_error = ValueError(f"HTTP {response.status} non-tracker response")
        except urllib.error.HTTPError as error:
            body = error.read(1024 * 1024)
            if looks_bencoded(body):
                return {
                    "status": "alive",
                    "latency_ms": round((time.monotonic() - started) * 1000, 1),
                    "ip_version": "unknown",
                    "detail": f"HTTP {error.code} bencoded tracker response",
                }
            last_error = error
        except Exception as error:  # noqa: BLE001
            last_error = error
    raise last_error or RuntimeError("no tracker response")


def websocket_accept(key: str) -> str:
    digest = hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest()
    return base64.b64encode(digest).decode()


def validate_websocket(parsed: urllib.parse.SplitResult, timeout: float) -> dict[str, Any]:
    port = parsed.port or (443 if parsed.scheme == "wss" else 80)
    host = parsed.hostname or ""
    path = urllib.parse.urlunsplit(("", "", parsed.path or "/announce", parsed.query, ""))
    last_error: Exception | None = None
    for family, kind, proto, sockaddr in resolve_addresses(host, port, socket.SOCK_STREAM):
        raw = socket.socket(family, kind, proto)
        raw.settimeout(timeout)
        started = time.monotonic()
        try:
            raw.connect(sockaddr)
            connection: socket.socket = raw
            if parsed.scheme == "wss":
                context = ssl.create_default_context()
                connection = context.wrap_socket(raw, server_hostname=host)
            key = base64.b64encode(os.urandom(16)).decode()
            request = (
                f"GET {path} HTTP/1.1\r\n"
                f"Host: {parsed.netloc}\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                f"Sec-WebSocket-Key: {key}\r\n"
                "Sec-WebSocket-Version: 13\r\n"
                "Sec-WebSocket-Protocol: bittorrent-tracker\r\n"
                "Origin: https://example.invalid\r\n\r\n"
            ).encode()
            connection.sendall(request)
            response = connection.recv(8192).decode("latin-1", "replace")
            headers = response.split("\r\n")
            if not headers or " 101 " not in headers[0]:
                raise ValueError(headers[0] if headers else "empty WebSocket response")
            expected = websocket_accept(key).lower()
            if not any(line.lower().strip() == f"sec-websocket-accept: {expected}" for line in headers[1:]):
                raise ValueError("invalid WebSocket accept header")
            return {
                "status": "alive",
                "latency_ms": round((time.monotonic() - started) * 1000, 1),
                "ip_version": address_family_name(family),
                "detail": "WebSocket 101 response",
            }
        except Exception as error:  # noqa: BLE001
            last_error = error
        finally:
            try:
                raw.close()
            except OSError:
                pass
    raise last_error or RuntimeError("DNS returned no addresses")


def validate_tracker(url: str, networks: set[str], timeout: float) -> dict[str, Any]:
    parsed = urllib.parse.urlsplit(url)
    if networks & {"i2p", "yggdrasil"}:
        return {
            "status": "unverified-special-network",
            "latency_ms": None,
            "ip_version": "special",
            "detail": "Requires a specialised network route unavailable in standard CI",
        }
    try:
        if parsed.scheme == "udp":
            return validate_udp(parsed, timeout)
        if parsed.scheme in {"http", "https"}:
            return validate_http(parsed, timeout)
        if parsed.scheme in WEBSOCKET_SCHEMES:
            return validate_websocket(parsed, timeout)
        raise ValueError("unsupported scheme")
    except Exception as error:  # noqa: BLE001
        return {
            "status": "unreachable",
            "latency_ms": None,
            "ip_version": "unknown",
            "detail": f"{type(error).__name__}: {str(error)[:180]}",
        }


def load_json(path: Path, fallback: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return fallback


def update_history(history: dict[str, Any], record: dict[str, Any], checked_at: str) -> dict[str, Any]:
    old = history.get(record["url"], {})
    checks = int(old.get("checks", 0)) + 1
    alive = record["status"] == "alive"
    successes = int(old.get("successes", 0)) + int(alive)
    old_ema = old.get("latency_ema_ms")
    current_latency = record.get("latency_ms")
    if alive and current_latency is not None:
        ema = current_latency if old_ema is None else round(float(old_ema) * 0.7 + float(current_latency) * 0.3, 1)
    else:
        ema = old_ema
    return {
        "checks": checks,
        "successes": successes,
        "success_rate": round(successes / checks, 4),
        "consecutive_failures": 0 if alive else int(old.get("consecutive_failures", 0)) + 1,
        "last_checked": checked_at,
        "last_seen": checked_at if alive else old.get("last_seen"),
        "latency_ema_ms": ema,
    }


def rank_score(record: dict[str, Any], history: dict[str, Any]) -> float:
    item = history.get(record["url"], {})
    rate = float(item.get("success_rate", 1.0))
    latency = float(item.get("latency_ema_ms") or record.get("latency_ms") or 5000)
    source_bonus = min(len(record["sources"]), 8) * 40
    scheme_bonus = {"udp": 45, "https": 35, "http": 15, "wss": 10, "ws": 0}.get(record["scheme"], 0)
    failure_penalty = int(item.get("consecutive_failures", 0)) * 150
    return round(rate * 1000 + source_bonus + scheme_bonus - latency / 10 - failure_penalty, 2)


def distinct_hosts(records: list[dict[str, Any]], limit: int | None = None) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    hosts: set[str] = set()
    for record in records:
        if record["host"] in hosts:
            continue
        hosts.add(record["host"])
        selected.append(record)
        if limit is not None and len(selected) >= limit:
            break
    return selected


def choose_primaries(records: list[dict[str, Any]], total: int = 12) -> list[dict[str, Any]]:
    quotas = {"udp": 6, "https": 4, "http": 2}
    chosen: list[dict[str, Any]] = []
    used_hosts: set[str] = set()
    for scheme, quota in quotas.items():
        for record in records:
            if record["scheme"] != scheme or record["host"] in used_hosts:
                continue
            chosen.append(record)
            used_hosts.add(record["host"])
            if sum(item["scheme"] == scheme for item in chosen) >= quota:
                break
    for record in records:
        if len(chosen) >= total:
            break
        if record["host"] not in used_hosts:
            chosen.append(record)
            used_hosts.add(record["host"])
    return chosen


def make_balanced_tiers(records: list[dict[str, Any]], tier_count: int = 12, backups: int = 2) -> list[list[str]]:
    primaries = choose_primaries(records, tier_count)
    used_hosts = {item["host"] for item in primaries}
    backup_pool = [item for item in records if item["host"] not in used_hosts]
    tiers = [[item["url"]] for item in primaries]
    index = 0
    for _ in range(backups):
        for tier in tiers:
            while index < len(backup_pool) and any(urllib.parse.urlsplit(url).hostname == backup_pool[index]["host"] for url in tier):
                index += 1
            if index >= len(backup_pool):
                return tiers
            tier.append(backup_pool[index]["url"])
            index += 1
    return tiers


def tier_text(tiers: list[list[str]]) -> str:
    return "\n\n".join("\n".join(tier) for tier in tiers) + ("\n" if tiers else "")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--workers", type=int, default=48)
    parser.add_argument("--aggressive-count", type=int, default=60)
    args = parser.parse_args()

    sources = json.loads(SOURCE_FILE.read_text(encoding="utf-8"))
    candidates: dict[str, dict[str, Any]] = {}
    source_results: list[dict[str, Any]] = []

    def fetch_source(source: dict[str, Any]) -> tuple[dict[str, Any], list[str], str | None]:
        try:
            text = fetch_text(source["url"])
            return source, extract_urls(text), None
        except Exception as error:  # noqa: BLE001
            return source, [], f"{type(error).__name__}: {str(error)[:180]}"

    with concurrent.futures.ThreadPoolExecutor(max_workers=min(12, len(sources))) as pool:
        fetched = list(pool.map(fetch_source, sources))

    for source, urls, error in fetched:
        source_results.append({
            "name": source["name"],
            "url": source["url"],
            "network": source["network"],
            "licence": source.get("licence", "Unknown"),
            "count": len(urls),
            "error": error,
        })
        for url in urls:
            entry = candidates.setdefault(url, {"sources": set(), "networks": set(), "tags": set()})
            entry["sources"].add(source["name"])
            entry["networks"].add(source["network"])
            entry["tags"].update(source.get("tags", []))

    if sum(result["error"] is None for result in source_results) < 2:
        raise RuntimeError("fewer than two tracker sources were available")

    checked_at = utc_now()
    items = sorted(candidates.items())

    def check(item: tuple[str, dict[str, Any]]) -> dict[str, Any]:
        url, metadata = item
        parsed = urllib.parse.urlsplit(url)
        validation = validate_tracker(url, metadata["networks"], args.timeout)
        return {
            "url": url,
            "scheme": parsed.scheme,
            "host": parsed.hostname or "",
            "port": parsed.port or {"http": 80, "https": 443, "ws": 80, "wss": 443}.get(parsed.scheme),
            "sources": sorted(metadata["sources"]),
            "networks": sorted(metadata["networks"]),
            "tags": sorted(metadata["tags"]),
            **validation,
        }

    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        records = list(pool.map(check, items))

    old_history = load_json(DATA_DIR / "history.json", {})
    history: dict[str, Any] = {}
    for record in records:
        history[record["url"]] = update_history(old_history, record, checked_at)
        record["score"] = rank_score(record, history)

    records.sort(key=lambda item: (-item["score"], item["url"]))
    transmission = [
        item for item in records
        if item["status"] == "alive"
        and item["scheme"] in TRANSMISSION_SCHEMES
        and "public" in item["networks"]
    ]
    webtorrent = [item for item in records if item["status"] == "alive" and item["scheme"] in WEBSOCKET_SCHEMES]
    unreachable = [item for item in records if item["status"] == "unreachable"]
    special = [item for item in records if item["status"] == "unverified-special-network"]

    all_candidates = sorted(item["url"] for item in records)
    write_lines(LIST_DIR / "candidates" / "all.txt", all_candidates)
    write_lines(LIST_DIR / "candidates" / "unreachable.txt", sorted(item["url"] for item in unreachable))
    write_lines(LIST_DIR / "transmission" / "all.txt", [item["url"] for item in transmission])
    for scheme in sorted(TRANSMISSION_SCHEMES):
        write_lines(LIST_DIR / "transmission" / f"{scheme}.txt", [item["url"] for item in transmission if item["scheme"] == scheme])

    distinct = distinct_hosts(transmission)
    best = distinct[:50]
    balanced_tiers = make_balanced_tiers(distinct, tier_count=12, backups=2)
    balanced_primaries = [tier[0] for tier in balanced_tiers]
    aggressive = distinct[: args.aggressive_count]
    atomic_write(LIST_DIR / "transmission" / "balanced.txt", tier_text(balanced_tiers))
    write_lines(LIST_DIR / "transmission" / "macos.txt", balanced_primaries)
    write_lines(LIST_DIR / "transmission" / "magnet.txt", balanced_primaries)
    write_lines(LIST_DIR / "transmission" / "best.txt", [item["url"] for item in best])
    write_lines(LIST_DIR / "transmission" / "aggressive.txt", [item["url"] for item in aggressive], blank_between=True)
    write_lines(LIST_DIR / "transmission" / "all-tiered.txt", [item["url"] for item in distinct], blank_between=True)

    write_lines(LIST_DIR / "webtorrent" / "all.txt", [item["url"] for item in webtorrent])
    for scheme in sorted(WEBSOCKET_SCHEMES):
        write_lines(LIST_DIR / "webtorrent" / f"{scheme}.txt", [item["url"] for item in webtorrent if item["scheme"] == scheme])
    for network in ("i2p", "yggdrasil"):
        write_lines(
            LIST_DIR / "special" / f"{network}.txt",
            sorted(item["url"] for item in special if network in item["networks"]),
        )

    by_source: dict[str, list[str]] = defaultdict(list)
    for record in records:
        for source in record["sources"]:
            by_source[source].append(record["url"])
    for source, urls in by_source.items():
        write_lines(LIST_DIR / "by-source" / f"{slugify(source)}.txt", sorted(urls))

    protocol_counts = Counter(item["scheme"] for item in records)
    alive_protocol_counts = Counter(item["scheme"] for item in records if item["status"] == "alive")
    summary = {
        "checked_at": checked_at,
        "source_count": len(sources),
        "source_successes": sum(result["error"] is None for result in source_results),
        "candidate_count": len(records),
        "alive_count": sum(item["status"] == "alive" for item in records),
        "transmission_count": len(transmission),
        "webtorrent_count": len(webtorrent),
        "special_network_count": len(special),
        "unreachable_count": len(unreachable),
        "balanced_tiers": len(balanced_tiers),
        "balanced_endpoints": sum(len(tier) for tier in balanced_tiers),
        "protocol_candidates": dict(sorted(protocol_counts.items())),
        "protocol_alive": dict(sorted(alive_protocol_counts.items())),
        "sources": source_results,
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    atomic_write(DATA_DIR / "status.json", json.dumps({"summary": summary, "trackers": records}, ensure_ascii=False, indent=2) + "\n")
    atomic_write(DATA_DIR / "history.json", json.dumps(history, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    atomic_write(DATA_DIR / "summary.json", json.dumps(summary, ensure_ascii=False, indent=2) + "\n")

    csv_path = DATA_DIR / "status.csv"
    temp_csv = csv_path.with_suffix(".csv.tmp")
    with temp_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "url", "status", "scheme", "host", "port", "latency_ms", "ip_version", "score", "sources", "networks", "tags", "detail"
        ], lineterminator="\n")
        writer.writeheader()
        for record in records:
            row = dict(record)
            row["sources"] = " | ".join(record["sources"])
            row["networks"] = " | ".join(record["networks"])
            row["tags"] = " | ".join(record["tags"])
            writer.writerow(row)
    temp_csv.replace(csv_path)

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
