# Alþjóðlegt Tracker-safn fyrir Transmission

[English](../../README.md) · [简体中文](../../README.zh-CN.md)

Verkefnið safnar opinberum BitTorrent Tracker-slóðum úr mörgum heimildum, varðveitir uppruna, prófar þær daglega og býr til skýra lista fyrir Transmission 4.1+, aðra BitTorrent-biðlara, WebTorrent og sérnet.

## Veldu réttan lista

| Listi | Notkun |
| --- | --- |
| [`macos.txt`](../../lists/transmission/macos.txt) | Transmission-viðmót á macOS; 12 valdir aðal-Trackerar. |
| [`magnet.txt`](../../lists/transmission/magnet.txt) | Bætt við Magnet URI án þess að tengillinn verði óhóflega langur. |
| [`balanced.txt`](../../lists/transmission/balanced.txt) | `default_trackers` með daemon/RPC; 12 samhliða tier með tveimur varaleiðum í hverju. |
| [`aggressive.txt`](../../lists/transmission/aggressive.txt) | Tímabundið fyrir sjaldgæfan eða veikan swarm; allt að 60 hýsingar. |
| [`all.txt`](../../lists/transmission/all.txt) | Allir UDP-, HTTP- og HTTPS-Trackerar sem standast nýjustu prófun. |
| [`candidates/all.txt`](../../lists/candidates/all.txt) | Allt safnið, líka óaðgengilegar slóðir; ekki flytja inn sem daglegan lista. |
| [`webtorrent/all.txt`](../../lists/webtorrent/all.txt) | WS/WSS fyrir WebTorrent; Transmission styður þau ekki. |
| [`special/`](../../lists/special/) | I2P/Yggdrasil aðeins með réttri netleið. |

## Bæta Trackerum við í Transmission macOS

1. Opnaðu [`macos.txt`](../../lists/transmission/macos.txt) og afritaðu allar 12 línurnar.
2. Veldu aðeins eitt verkefni í Transmission.
3. Opnaðu **View → Show Inspector** og flipann **Trackers**.
4. Ýttu á **+**, límdu línurnar í nýja reitinn og staðfestu.
5. Hver lína verður sjálfstætt tier. Bíddu í nokkrar mínútur eftir announce og peer discovery.

Notaðu `macos.txt` hér. Ef `balanced.txt` er límt í macOS-viðmótið tapast varaskipanin. Private torrent banna oft DHT, PeX og utanaðkomandi Trackera; fylgdu reglum síðunnar.

## Styrkja Magnet-tengil

```bash
git clone https://github.com/cyriusweng/transmission-global-trackers.git
cd transmission-global-trackers
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
python3 scripts/boost_magnet.py --profile balanced --open 'magnet:?xt=urn:btih:...'
```

Skipunin prentar nýjan Magnet. `balanced` bætir við 12 Trackerum, `aggressive` allt að 60 og `all` öllum staðfestum til greiningar. Núverandi `tr=` gildi haldast og tvítekningar hverfa.

## Varanlegir sjálfgefnir Trackerar

`default_trackers` fylgir BEP 12: eitt línuskil er varaleið í sama tier, auð lína býr til nýtt samhliða tier. Notaðu [`balanced.txt`](../../lists/transmission/balanced.txt) með daemon/RPC. Innbyggða macOS-viðmótið hefur engan varanlegan alþjóðlegan reit; notaðu `macos.txt` á hvert verkefni eða styrktu Magnet fyrst.

## Aðrir biðlarar

qBittorrent, Deluge og BiglyBT geta notað [`best.txt`](../../lists/transmission/best.txt) eða [`all.txt`](../../lists/transmission/all.txt). aria2/Motrix nota `all.txt` eða tilskilið kommusnið. WebTorrent notar `webtorrent/all.txt`.

## Sjálfvirk uppfærsla

GitHub Actions keyrir daglega kl. 03:17 UTC; tölvan þín má vera slökkt. Cloud Runner safnar, framkvæmir létta samskiptaprófun, uppfærir sögu, keyrir próf og sendir commit. Hann sækir ekki Torrent-efni og skráir sig ekki sem peer. Niðurstöður geta verið mismunandi eftir landi, ISP, VPN og IPv6.

## Takmörk og persónuvernd

„Alive“ staðfestir aðeins gilt svar í síðustu prófun; það tryggir hvorki peer-a né fullan seed fyrir infohash. Tracker getur ekki búið til gögn sem vantar í allan swarm. Stórir listar sýna fleiri rekstraraðilum infohash. Persónulegt passkey er aðgangsupplýsing og er útilokað.

Endurbygging á staðnum án aukapakka:

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests
```
