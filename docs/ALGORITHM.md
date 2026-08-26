# Validation and tier algorithm

## Pipeline

1. Fetch every fixed source in `sources.json`.
2. Extract UDP, HTTP, HTTPS, WS and WSS announce URLs.
3. Normalise schemes, hosts, ports and paths; reject local/private addresses and malformed URLs.
4. Deduplicate globally while retaining every source and topic tag attached to each endpoint.
5. Run one lightweight protocol check:
   - UDP: BEP 15 connection handshake;
   - HTTP/HTTPS: scrape request, followed by a deliberately incomplete announce request when scrape is unavailable; only a tracker-shaped bencoded response counts;
   - WS/WSS: WebSocket upgrade using the `bittorrent-tracker` subprotocol;
   - I2P/Yggdrasil: retain without ordinary-internet validation.
6. Update persistent health history and generate purpose-specific lists.

No check downloads torrent payloads or announces this runner as a peer.

## Ranking

A verified endpoint receives a score based on:

- rolling success rate;
- exponentially smoothed response latency;
- number of independent source feeds containing it;
- protocol preference for Transmission;
- consecutive failures.

The first run is necessarily dominated by current reachability and cross-source agreement. Daily checks gradually give long-term reliability more weight. A temporary outage remains visible in the complete candidate inventory and history.

## Host diversity

Recommended profiles select at most one endpoint per hostname. This prevents one operator with many ports or protocols from occupying most high-ranked positions and reduces correlated failure.

## Transmission tier layouts

Transmission implements BEP 12:

- a single newline places trackers in the same fallback tier;
- a blank line starts another tier queried in parallel.

### Balanced

- 12 parallel primary tiers;
- target primary mix: 6 UDP, 4 HTTPS and 2 HTTP;
- up to two fallback trackers per tier;
- 36 endpoints at most;
- distinct hosts throughout the selected set.

This profile contacts only the primary tracker in each tier unless it needs a fallback.

### Aggressive

The 60 highest-ranked distinct hosts are emitted as independent tiers. Transmission can contact them in parallel. This improves the chance of finding a rare swarm at the cost of more requests, timeouts and infohash exposure.

### All tiered

Every currently verified, distinct Transmission-compatible host becomes an independent tier. This is a diagnostic artefact rather than a recommended permanent default.

## Why full aggregation and daily defaults are separate

The complete inventory serves archival, regional, research and unusual-client needs. A default client profile serves responsiveness and predictable network behaviour. Keeping both preserves coverage without forcing every user to query every tracker for every torrent.
