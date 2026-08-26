# Transmission-erako Tracker bilduma globala

[English](../../README.md)

Proiektuak BitTorrent Tracker publikoak hainbat iturritatik biltzen ditu, bikoiztuak kentzen ditu, egunero egiaztatzen ditu eta Transmission 4.1+ programarako antolaketa egokiak sortzen ditu.

- [`balanced`](../../lists/transmission/balanced.txt): eguneroko erabilerarako gomendatua; maila paralelo gutxi eta ordezko Tracker-ak.
- [`aggressive`](../../lists/transmission/aggressive.txt): aldi baterako, swarm arraro edo ahulentzat.
- [`all`](../../lists/transmission/all.txt): une honetan egiaztatutako UDP, HTTP eta HTTPS Tracker guztiak.
- [`candidates`](../../lists/candidates/all.txt): inbentario osoa, une honetan lineaz kanpo dauden helbideak barne.

Magnet esteka bati Tracker-ak gehitzeko:

```bash
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
```

Passkey pertsonala duten Tracker pribatuak ez dira argitaratzen. “Alive” egoerak azken egiaztapenean erantzun balioduna jaso dela baino ez du adierazten; ez du Torrent jakin baterako peer edo seed osoa bermatzen.
