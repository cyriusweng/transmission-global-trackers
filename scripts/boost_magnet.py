#!/usr/bin/env python3
"""Append a generated tracker profile to a magnet URI without duplicating trackers."""

from __future__ import annotations

import argparse
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILES = {
    "balanced": ROOT / "lists" / "transmission" / "balanced.txt",
    "aggressive": ROOT / "lists" / "transmission" / "aggressive.txt",
    "all": ROOT / "lists" / "transmission" / "all.txt",
}


def tracker_urls(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def boost(magnet: str, trackers: list[str]) -> str:
    parsed = urllib.parse.urlsplit(magnet.strip())
    if parsed.scheme.lower() != "magnet":
        raise ValueError("input is not a magnet URI")
    pairs = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    existing = {value for key, value in pairs if key == "tr"}
    pairs.extend(("tr", tracker) for tracker in trackers if tracker not in existing)
    query = urllib.parse.urlencode(pairs, doseq=True, safe="/:[]")
    return urllib.parse.urlunsplit(("magnet", "", parsed.path, query, ""))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("magnet", nargs="?", help="Magnet URI; reads stdin when omitted")
    parser.add_argument("--profile", choices=sorted(PROFILES), default="balanced")
    args = parser.parse_args()
    magnet = args.magnet or sys.stdin.read().strip()
    if not magnet:
        parser.error("a magnet URI is required")
    print(boost(magnet, tracker_urls(PROFILES[args.profile])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
