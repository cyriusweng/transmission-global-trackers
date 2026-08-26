# Transmission Global Trackers

**Languages:** [English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](docs/i18n/README.zh-TW.md) · [Español](docs/i18n/README.es.md) · [Français](docs/i18n/README.fr.md) · [Deutsch](docs/i18n/README.de.md) · [Português](docs/i18n/README.pt-BR.md) · [Русский](docs/i18n/README.ru.md) · [日本語](docs/i18n/README.ja.md) · [한국어](docs/i18n/README.ko.md) · [العربية](docs/i18n/README.ar.md) · [فارسی](docs/i18n/README.fa.md) · [हिन्दी](docs/i18n/README.hi.md) · [Bahasa Indonesia](docs/i18n/README.id.md) · [Türkçe](docs/i18n/README.tr.md) · [Tiếng Việt](docs/i18n/README.vi.md) · [Українська](docs/i18n/README.uk.md) · [Esperanto](docs/i18n/README.eo.md) · [Íslenska](docs/i18n/README.is.md) · [Euskara](docs/i18n/README.eu.md) · [Cymraeg](docs/i18n/README.cy.md)

A comprehensive, source-attributed and continuously validated collection of public BitTorrent trackers. It preserves the full candidate inventory while producing practical lists for Transmission 4.1+, other conventional BitTorrent clients, WebTorrent and specialised networks.

## Choose the right list

| List | Use it when |
| --- | --- |
| [`macos.txt`](lists/transmission/macos.txt) | You use the Transmission macOS interface. It contains 12 high-ranked primary trackers that can be pasted safely into one transfer. |
| [`magnet.txt`](lists/transmission/magnet.txt) | You want to add trackers to a Magnet URI. It contains the same 12 primaries and avoids an oversized Magnet link. |
| [`balanced.txt`](lists/transmission/balanced.txt) | You can set Transmission's `default_trackers` through a daemon configuration or RPC. It contains 12 parallel tiers, each with two fallbacks. |
| [`aggressive.txt`](lists/transmission/aggressive.txt) | A rare torrent has few or no discoverable peers. Use temporarily; it queries up to 60 independent tracker hosts. |
| [`all.txt`](lists/transmission/all.txt) | You need every currently verified UDP, HTTP and HTTPS tracker, one per line. |
| [`all-tiered.txt`](lists/transmission/all-tiered.txt) | You are diagnosing a weak swarm and deliberately want every verified host as a separate parallel tier. |
| [`candidates/all.txt`](lists/candidates/all.txt) | You need the complete deduplicated source inventory, including endpoints currently offline. Do not paste this into a client as a daily list. |
| [`webtorrent/all.txt`](lists/webtorrent/all.txt) | You use a WebTorrent client that supports WS/WSS trackers. Transmission does not support these protocols. |
| [`special/`](lists/special/) | You use I2P or Yggdrasil and have the required network route. Ordinary GitHub runners cannot validate these endpoints. |
| [`status.csv`](data/status.csv) | You need status, latency, score, source attribution and diagnostic detail in machine-readable form. |

## Transmission on macOS: add trackers to an existing transfer

1. Open [`macos.txt`](lists/transmission/macos.txt) and copy all 12 lines.
2. In Transmission, select **one** transfer.
3. Choose **View → Show Inspector**, then open the **Trackers** tab.
4. Click the **+** button. Paste the copied lines into the new tracker field and confirm.
5. Transmission adds each pasted line as a separate tracker tier. Allow a few minutes for announces and peer discovery.

Use `macos.txt` for this workflow. Pasting `balanced.txt` into the macOS tracker field flattens its fallback structure, so it provides no benefit over the smaller macOS list.

Private torrents normally restrict DHT, PeX and outside trackers. Do not add public trackers to a private torrent unless that tracker's rules explicitly permit it.

## Add trackers to a Magnet URI

Clone the repository once:

```bash
git clone https://github.com/cyriusweng/transmission-global-trackers.git
cd transmission-global-trackers
```

Generate a balanced Magnet URI:

```bash
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
python3 scripts/boost_magnet.py --profile balanced --open 'magnet:?xt=urn:btih:...'
```

The first command prints a new Magnet URI with the 12 entries from `magnet.txt`. The second uses `--open` to hand the result directly to Transmission on macOS; Transmission then follows its normal add-transfer preferences. Available profiles are:

- `balanced`: 12 primary trackers; recommended;
- `aggressive`: up to 60 trackers for rare swarms;
- `all`: every verified Transmission-compatible tracker; diagnostic use only.

Existing `tr=` parameters are preserved and duplicates are removed.

## Persistent default trackers

Transmission's `default_trackers` setting follows [BEP 12](https://www.bittorrent.org/beps/bep_0012.html):

- one newline means a fallback tracker in the same tier;
- one blank line starts another tier queried in parallel.

Use the exact contents of [`balanced.txt`](lists/transmission/balanced.txt) with `default_trackers` when your Transmission daemon, RPC controller or frontend exposes that setting. The native macOS interface does not currently expose a persistent global default-trackers field; use `macos.txt` per transfer or boost the Magnet URI instead.

## Other BitTorrent clients

The repository is not limited to Transmission:

- **qBittorrent, Deluge, BiglyBT and similar clients:** start with [`best.txt`](lists/transmission/best.txt) or [`all.txt`](lists/transmission/all.txt), according to the client's import format.
- **aria2 and Motrix:** use [`all.txt`](lists/transmission/all.txt) or the comma-separated format required by that application.
- **WebTorrent:** use [`webtorrent/all.txt`](lists/webtorrent/all.txt).
- **I2P/Yggdrasil:** use the matching file under [`special/`](lists/special/) only when that network is configured.

UDP, HTTP and HTTPS are standard BitTorrent tracker protocols. WS and WSS are kept separate because conventional Transmission does not use WebTorrent trackers.

## How the lists are built

Every scheduled run:

1. fetches all fixed sources in [`sources.json`](sources.json);
2. extracts and normalises tracker URLs;
3. deduplicates them while retaining every source and tag;
4. performs one lightweight protocol check per endpoint;
5. updates historical success and latency data;
6. ranks trackers and rebuilds every profile.

Validation uses a BEP 15 handshake for UDP, tracker-shaped bencoded responses for HTTP/HTTPS, and a WebSocket upgrade for WS/WSS. It downloads no torrent payload and does not register the runner as a peer. The full method and ranking rules are documented in [`docs/ALGORITHM.md`](docs/ALGORITHM.md).

## Automatic daily updates

GitHub Actions runs the refresh workflow every day at **03:17 UTC**. Your computer does not need to be on. GitHub-hosted runners fetch, validate, test and commit changed generated files using the repository's built-in `GITHUB_TOKEN`.

You can also run it manually from **Actions → Refresh tracker health → Run workflow**.

The result reflects connectivity from a GitHub cloud runner. A tracker may behave differently on another ISP, country, VPN or IPv6 route.

## Accuracy, privacy and limits

- “Alive” means the endpoint returned a protocol-valid response during the latest check.
- It does not prove that a particular infohash has peers or a complete seed.
- More trackers cannot reconstruct data missing from every peer in a swarm.
- Aggressive and all-tier profiles expose an infohash to more tracker operators and create more network requests.
- Private trackers containing personal passkeys are excluded because those URLs are account credentials and cannot be published safely.
- Offline endpoints remain in the candidate inventory so regional and intermittent trackers are not silently lost.

## Update locally

No third-party Python packages are required:

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests
```

Source additions are welcome through pull requests. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the rules.

## Licence and attribution

[`sources.json`](sources.json) records each source URL and source licence. Generated records retain source attribution. Project code is released under GPL-3.0-or-later.
