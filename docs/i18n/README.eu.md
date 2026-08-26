# Transmission-erako Tracker bilduma globala

[English](../../README.md) · [简体中文](../../README.zh-CN.md)

Proiektuak BitTorrent Tracker publikoak hainbat iturritatik biltzen ditu, jatorriaren informazioa gordetzen du, egunero egiaztatzen ditu eta Transmission 4.1+, beste BitTorrent bezero, WebTorrent eta sare berezietarako zerrenda argiak sortzen ditu.

## Aukeratu zerrenda egokia

| Zerrenda | Erabilera |
| --- | --- |
| [`macos.txt`](../../lists/transmission/macos.txt) | Transmission-en macOS interfazea; hautatutako 12 Tracker nagusi. |
| [`magnet.txt`](../../lists/transmission/magnet.txt) | Magnet URI bati gehitzeko, esteka gehiegi luzatu gabe. |
| [`balanced.txt`](../../lists/transmission/balanced.txt) | daemon/RPC bidezko `default_trackers`; 12 maila paralelo, bakoitzean bi ordezko. |
| [`aggressive.txt`](../../lists/transmission/aggressive.txt) | Aldi baterako swarm arraro edo ahulentzat; gehienez 60 host. |
| [`all.txt`](../../lists/transmission/all.txt) | Une honetan egiaztatutako UDP, HTTP eta HTTPS Tracker guztiak. |
| [`candidates/all.txt`](../../lists/candidates/all.txt) | Inbentario osoa, une honetan lineaz kanpo daudenak barne; ez inportatu eguneroko zerrenda gisa. |
| [`webtorrent/all.txt`](../../lists/webtorrent/all.txt) | WebTorrent-erako WS/WSS; Transmission-ek ez ditu onartzen. |
| [`special/`](../../lists/special/) | I2P/Yggdrasil dagokion sare-bidea konfiguratuta dagoenean bakarrik. |

## Tracker-ak gehitu Transmission macOS-en

1. Ireki [`macos.txt`](../../lists/transmission/macos.txt) eta kopiatu 12 lerroak.
2. Hautatu transferentzia bakarra Transmission-en.
3. Ireki **View → Show Inspector** eta **Trackers** fitxa.
4. Sakatu **+**, itsatsi lerroak eremu berrian eta baieztatu.
5. Lerro bakoitza maila independentea bihurtzen da. Itxaron minutu batzuk announce eta peer discovery egiteko.

Erabili `macos.txt`. `balanced.txt` macOS interfazean itsasteak ordezko mailen egitura galtzen du. Private torrent-ek normalean DHT, PeX eta kanpoko Tracker-ak debekatzen dituzte; bete gunearen arauak.

## Magnet esteka indartu

```bash
git clone https://github.com/cyriusweng/transmission-global-trackers.git
cd transmission-global-trackers
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
python3 scripts/boost_magnet.py --profile balanced --open 'magnet:?xt=urn:btih:...'
```

Komandoak Magnet berria inprimatzen du. `balanced`-ek 12 Tracker gehitzen ditu, `aggressive`-k 60 arte eta `all`-ek egiaztatutako guztiak diagnostikorako. Lehendik dauden `tr=` parametroak gordetzen dira eta bikoiztuak kentzen dira.

## Tracker lehenetsi iraunkorrak

`default_trackers`-ek BEP 12 jarraitzen du: lerro-jauzi batek maila bereko ordezkoa adierazten du, lerro hutsak maila paralelo berria sortzen du. Erabili [`balanced.txt`](../../lists/transmission/balanced.txt) daemon/RPC bidez. macOS interfazeak ez du eremu global iraunkorrik; erabili `macos.txt` transferentzia bakoitzean edo indartu Magnet aurretik.

## Beste bezero batzuk

qBittorrent, Deluge eta BiglyBT-k [`best.txt`](../../lists/transmission/best.txt) edo [`all.txt`](../../lists/transmission/all.txt) erabil dezakete. aria2/Motrix-ek `all.txt` edo behar den koma-formatua erabiltzen dute. WebTorrent-ek `webtorrent/all.txt` erabiltzen du.

## Eguneratze automatikoa

GitHub Actions egunero 03:17 UTC-n exekutatzen da; zure ordenagailua itzalita egon daiteke. Cloud Runner-ek iturriak biltzen ditu, protokolo-egiaztapen arina egiten du, historia eguneratu, testak exekutatu eta commit bidaltzen du. Ez du Torrent edukirik deskargatzen eta ez da peer gisa erregistratzen. Emaitzak herrialde, ISP, VPN eta IPv6-ren arabera alda daitezke.

## Mugak eta pribatutasuna

“Alive” azken egiaztapeneko erantzun baliozkoa baino ez da; ez du infohash baterako peer edo seed osoa bermatzen. Tracker batek ezin ditu swarm osoan falta diren datuak sortu. Zerrenda handiek infohash operadore gehiagori erakusten diote. Passkey pertsonala kontu-kredentziala da eta baztertzen da.

Tokiko berreraikuntza pakete gehigarririk gabe:

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests
```
