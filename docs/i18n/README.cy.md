# Casgliad Tracker byd-eang ar gyfer Transmission

[English](../../README.md)

Mae'r prosiect yn casglu Trackerau BitTorrent cyhoeddus o sawl ffynhonnell, yn dileu dyblygiadau, yn eu gwirio bob dydd ac yn creu trefniadau addas ar gyfer Transmission 4.1+.

- [`balanced`](../../lists/transmission/balanced.txt): yr opsiwn a argymhellir bob dydd; ychydig o haenau cyfochrog gyda Trackerau wrth gefn.
- [`aggressive`](../../lists/transmission/aggressive.txt): defnydd dros dro ar gyfer swarm prin neu wan.
- [`all`](../../lists/transmission/all.txt): pob Tracker UDP, HTTP a HTTPS sydd wedi'i wirio ar hyn o bryd.
- [`candidates`](../../lists/candidates/all.txt): y rhestr gyflawn, gan gynnwys cyfeiriadau sydd all-lein ar hyn o bryd.

Ychwanegu Trackerau at ddolen Magnet:

```bash
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
```

Ni chyhoeddir Trackerau preifat sy'n cynnwys passkey personol. Mae “Alive” yn cadarnhau ymateb dilys yn y prawf diweddaraf yn unig; nid yw'n gwarantu peer na seed cyflawn ar gyfer Torrent penodol.
