# Tutmondaj spuriloj por Transmission

[English](../../README.md) · [简体中文](../../README.zh-CN.md)

La projekto kolektas publikajn BitTorrent-spurilojn el pluraj fontoj, konservas la devenon, kontrolas ilin ĉiutage kaj generas klarajn listojn por Transmission 4.1+, aliaj BitTorrent-klientoj, WebTorrent kaj specialaj retoj.

## Elektu la ĝustan liston

| Listo | Uzo |
| --- | --- |
| [`macos.txt`](../../lists/transmission/macos.txt) | Transmission-interfaco en macOS; 12 elektitaj ĉefaj spuriloj. |
| [`magnet.txt`](../../lists/transmission/magnet.txt) | Aldono al Magnet-URI sen tro longa ligilo. |
| [`balanced.txt`](../../lists/transmission/balanced.txt) | `default_trackers` per daemon/RPC; 12 paralelaj niveloj kun du rezervoj en ĉiu. |
| [`aggressive.txt`](../../lists/transmission/aggressive.txt) | Provizore por rara aŭ malforta svarmo; ĝis 60 gastigantoj. |
| [`all.txt`](../../lists/transmission/all.txt) | Ĉiuj nun kontrolitaj UDP-, HTTP- kaj HTTPS-spuriloj. |
| [`candidates/all.txt`](../../lists/candidates/all.txt) | Plena inventaro, ankaŭ nun neatingeblaj adresoj; ne importu kiel ĉiutagan liston. |
| [`webtorrent/all.txt`](../../lists/webtorrent/all.txt) | WS/WSS por WebTorrent; Transmission ne subtenas ilin. |
| [`special/`](../../lists/special/) | I2P/Yggdrasil nur kun agordita reta vojo. |

## Aldoni spurilojn en Transmission macOS

1. Malfermu [`macos.txt`](../../lists/transmission/macos.txt) kaj kopiu ĉiujn 12 liniojn.
2. Elektu nur unu transdonon en Transmission.
3. Malfermu **View → Show Inspector**, poste la langeton **Trackers**.
4. Premu **+**, algluu la liniojn en la novan kampon kaj konfirmu.
5. Ĉiu linio fariĝas aparta nivelo. Atendu kelkajn minutojn por announce kaj trovo de samranguloj.

Uzu `macos.txt` por ĉi tiu metodo. Alglui `balanced.txt` en la macOS-interfacon platigas la rezervan strukturon. Privataj torentoj ofte malpermesas DHT, PeX kaj eksterajn spurilojn; sekvu la regulojn de la retejo.

## Plifortigi Magnet-ligilon

```bash
git clone https://github.com/cyriusweng/transmission-global-trackers.git
cd transmission-global-trackers
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
python3 scripts/boost_magnet.py --profile balanced --open 'magnet:?xt=urn:btih:...'
```

La komando eldonas novan Magnet-ligilon. `balanced` aldonas 12 spurilojn, `aggressive` ĝis 60, kaj `all` ĉiujn kontrolitajn por diagnozo. Ekzistantaj `tr=` parametroj restas kaj duoblaĵoj estas forigitaj.

## Daŭraj defaŭltaj spuriloj

`default_trackers` sekvas BEP 12: unu linifino signifas rezervon en la sama nivelo, malplena linio kreas novan paralelan nivelon. Uzu [`balanced.txt`](../../lists/transmission/balanced.txt) per daemon/RPC. La denaska macOS-interfaco ne havas daŭran tutmondan kampon; uzu `macos.txt` por ĉiu transdono aŭ plifortigu la Magnet-ligilon.

## Aliaj klientoj

qBittorrent, Deluge kaj BiglyBT povas uzi [`best.txt`](../../lists/transmission/best.txt) aŭ [`all.txt`](../../lists/transmission/all.txt). aria2/Motrix uzas `all.txt` aŭ la bezonatan koman formaton. WebTorrent uzas `webtorrent/all.txt`.

## Aŭtomata ĝisdatigo

GitHub Actions funkcias ĉiutage je 03:17 UTC; via komputilo povas esti malŝaltita. Nuba Runner kolektas, faras malpezan protokolkontrolon, ĝisdatigas historion, testas kaj sendas commit. Ĝi ne elŝutas torentan enhavon kaj ne registriĝas kiel peer. Rezultoj povas varii laŭ lando, ISP, VPN kaj IPv6.

## Limoj kaj privateco

“Alive” nur konfirmas validan respondon en la lasta kontrolo; ĝi ne garantias samrangulojn aŭ kompletan seed por infohash. Spurilo ne povas rekrei datumojn mankantajn en la tuta svarmo. Grandaj profiloj montras la infohash al pli da funkciigistoj. Persona passkey estas konta akreditaĵo kaj estas ekskludita.

Loka rekonstruo sen kromaj pakaĵoj:

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests
```
