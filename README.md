# Transmission Global Trackers

**Languages:** [English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](docs/i18n/README.zh-TW.md) · [Español](docs/i18n/README.es.md) · [Français](docs/i18n/README.fr.md) · [Deutsch](docs/i18n/README.de.md) · [Português](docs/i18n/README.pt-BR.md) · [Русский](docs/i18n/README.ru.md) · [日本語](docs/i18n/README.ja.md) · [한국어](docs/i18n/README.ko.md) · [العربية](docs/i18n/README.ar.md) · [فارسی](docs/i18n/README.fa.md) · [हिन्दी](docs/i18n/README.hi.md) · [Bahasa Indonesia](docs/i18n/README.id.md) · [Türkçe](docs/i18n/README.tr.md) · [Tiếng Việt](docs/i18n/README.vi.md) · [Українська](docs/i18n/README.uk.md) · [Esperanto](docs/i18n/README.eo.md) · [Íslenska](docs/i18n/README.is.md) · [Euskara](docs/i18n/README.eu.md) · [Cymraeg](docs/i18n/README.cy.md)

A comprehensive, source-attributed and continuously validated collection of public BitTorrent trackers, with layouts designed specifically for Transmission 4.1+.

## What this repository provides

| List | Purpose |
| --- | --- |
| [`balanced.txt`](lists/transmission/balanced.txt) | Recommended default. Twelve parallel tiers, each with fallback trackers. Strong discovery without contacting every endpoint at once. |
| [`aggressive.txt`](lists/transmission/aggressive.txt) | More independent tiers for rare or weak swarms. Use temporarily. |
| [`all-tiered.txt`](lists/transmission/all-tiered.txt) | Every currently verified Transmission-compatible tracker as an independent tier. Diagnostic use only. |
| [`all.txt`](lists/transmission/all.txt) | Every currently verified HTTP, HTTPS and UDP tracker, one per line. |
| [`candidates/all.txt`](lists/candidates/all.txt) | Full deduplicated aggregation, including endpoints that are currently offline. |
| [`webtorrent/all.txt`](lists/webtorrent/all.txt) | Verified WS/WSS trackers for WebTorrent clients. Transmission does not support these. |
| [`special/`](lists/special/) | I2P and Yggdrasil candidates. Standard GitHub runners cannot validate these networks. |
| [`status.csv`](data/status.csv) | Machine-readable status, latency, score, sources and diagnostic detail. |

Private trackers containing personal passkeys are intentionally excluded. They are account-specific credentials and cannot be safely or usefully published.

## Optimised Transmission tiers

Transmission follows [BEP 12](https://www.bittorrent.org/beps/bep_0012.html):

- one newline means fallback trackers within the same tier;
- one blank line means a separate tier queried in parallel.

The balanced profile therefore uses a small number of parallel primary trackers and keeps additional endpoints as fallbacks. Ranking combines current reachability, historical success rate, latency, protocol, hostname diversity and the number of independent sources containing an endpoint. The complete method is documented in [`docs/ALGORITHM.md`](docs/ALGORITHM.md).

Use `aggressive.txt` when a torrent has few peers. Return to `balanced.txt` afterwards. Large tracker lists cannot revive a swarm that has no complete seed.

## Add trackers to a magnet URI

```bash
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
```

Available profiles are `balanced`, `aggressive` and `all`.

## Update locally

No third-party Python packages are required.

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests
```

The scheduled GitHub Action refreshes the lists daily. Validation is deliberately lightweight: one protocol handshake per endpoint, with no payload download and no peer registration.

## Compatibility

- **Transmission:** UDP, HTTP and HTTPS lists under `lists/transmission/`
- **WebTorrent clients:** WS and WSS lists under `lists/webtorrent/`
- **I2P/Yggdrasil:** retained separately and not claimed as validated by ordinary internet runners

## Sources and attribution

The full source inventory, URLs and source licences are recorded in [`sources.json`](sources.json) and in each generated status report. Generated tracker data retains its source attribution. Project code is released under GPL-3.0-or-later.

## Accuracy boundary

Tracker health changes continuously. “Alive” means the endpoint returned a protocol-valid response during the latest check. It does not guarantee that a particular infohash has peers, that a peer is a complete seed, or that the endpoint is reachable from every network.
