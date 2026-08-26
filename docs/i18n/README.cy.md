# Casgliad Tracker byd-eang ar gyfer Transmission

[English](../../README.md) · [简体中文](../../README.zh-CN.md)

Mae'r prosiect yn casglu Trackerau BitTorrent cyhoeddus o sawl ffynhonnell, yn cadw'r priodoliad, yn eu gwirio bob dydd ac yn creu rhestrau clir ar gyfer Transmission 4.1+, cleientiaid BitTorrent eraill, WebTorrent a rhwydweithiau arbenigol.

## Dewis y rhestr gywir

| Rhestr | Defnydd |
| --- | --- |
| [`macos.txt`](../../lists/transmission/macos.txt) | Rhyngwyneb Transmission ar macOS; 12 prif Tracker dethol. |
| [`magnet.txt`](../../lists/transmission/magnet.txt) | Ychwanegu at Magnet URI heb wneud y ddolen yn rhy hir. |
| [`balanced.txt`](../../lists/transmission/balanced.txt) | `default_trackers` drwy daemon/RPC; 12 haen gyfochrog gyda dau wrth gefn ym mhob un. |
| [`aggressive.txt`](../../lists/transmission/aggressive.txt) | Dros dro ar gyfer swarm prin neu wan; hyd at 60 host. |
| [`all.txt`](../../lists/transmission/all.txt) | Pob Tracker UDP, HTTP a HTTPS sydd wedi'i wirio ar hyn o bryd. |
| [`candidates/all.txt`](../../lists/candidates/all.txt) | Y rhestr gyflawn, gan gynnwys endpointau all-lein; peidiwch â'i mewnforio fel rhestr ddyddiol. |
| [`webtorrent/all.txt`](../../lists/webtorrent/all.txt) | WS/WSS ar gyfer WebTorrent; nid yw Transmission yn eu cefnogi. |
| [`special/`](../../lists/special/) | I2P/Yggdrasil dim ond pan fo'r llwybr rhwydwaith wedi'i osod. |

## Ychwanegu Trackerau yn Transmission macOS

1. Agorwch [`macos.txt`](../../lists/transmission/macos.txt) a chopïwch y 12 llinell.
2. Dewiswch un trosglwyddiad yn unig yn Transmission.
3. Agorwch **View → Show Inspector**, yna'r tab **Trackers**.
4. Pwyswch **+**, gludwch y llinellau yn y maes newydd a chadarnhewch.
5. Daw pob llinell yn haen annibynnol. Arhoswch ychydig funudau am announce a peer discovery.

Defnyddiwch `macos.txt` yma. Mae gludo `balanced.txt` yn rhyngwyneb macOS yn gwastatáu'r strwythur wrth gefn. Mae private torrent fel arfer yn gwahardd DHT, PeX a Trackerau allanol; dilynwch reolau'r safle.

## Cryfhau dolen Magnet

```bash
git clone https://github.com/cyriusweng/transmission-global-trackers.git
cd transmission-global-trackers
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
python3 scripts/boost_magnet.py --profile balanced --open 'magnet:?xt=urn:btih:...'
```

Mae'r gorchymyn yn argraffu Magnet newydd. Mae `balanced` yn ychwanegu 12 Tracker, `aggressive` hyd at 60, ac `all` bob Tracker dilys ar gyfer diagnosis. Cedwir paramedrau `tr=` presennol a chaiff dyblygiadau eu tynnu.

## Trackerau diofyn parhaol

Mae `default_trackers` yn dilyn BEP 12: mae un llinell newydd yn wrth gefn yn yr un haen, ac mae llinell wag yn creu haen gyfochrog newydd. Defnyddiwch [`balanced.txt`](../../lists/transmission/balanced.txt) gyda daemon/RPC. Nid oes maes byd-eang parhaol yn rhyngwyneb macOS; defnyddiwch `macos.txt` fesul trosglwyddiad neu gryfhau'r Magnet yn gyntaf.

## Cleientiaid eraill

Gall qBittorrent, Deluge a BiglyBT ddefnyddio [`best.txt`](../../lists/transmission/best.txt) neu [`all.txt`](../../lists/transmission/all.txt). Mae aria2/Motrix yn defnyddio `all.txt` neu'r fformat coma gofynnol. Mae WebTorrent yn defnyddio `webtorrent/all.txt`.

## Diweddaru awtomatig

Mae GitHub Actions yn rhedeg bob dydd am 03:17 UTC; gall eich cyfrifiadur fod wedi'i ddiffodd. Mae'r Cloud Runner yn casglu, yn gwneud gwiriad protocol ysgafn, yn diweddaru hanes, yn rhedeg profion ac yn anfon commit. Nid yw'n lawrlwytho cynnwys Torrent nac yn cofrestru fel peer. Gall y canlyniad amrywio yn ôl gwlad, ISP, VPN ac IPv6.

## Terfynau a phreifatrwydd

Mae “Alive” ond yn cadarnhau ymateb dilys yn y prawf diwethaf; nid yw'n gwarantu peer na seed cyflawn ar gyfer infohash. Ni all Tracker greu data sydd ar goll o'r swarm cyfan. Mae rhestrau mawr yn datgelu'r infohash i fwy o weithredwyr. Mae passkey personol yn fanylyn cyfrif ac felly'n cael ei eithrio.

Ailadeiladu lleol heb becynnau ychwanegol:

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests
```
