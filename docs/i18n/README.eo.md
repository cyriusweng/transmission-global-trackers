# Tutmondaj spuriloj por Transmission

[English](../../README.md)

La projekto kolektas publikajn BitTorrent-spurilojn el pluraj fontoj, forigas duoblaĵojn, kontrolas ilin ĉiutage kaj generas aranĝojn optimumigitajn por Transmission 4.1+.

- [`balanced`](../../lists/transmission/balanced.txt): rekomendita por ĉiutaga uzo; malmultaj paralelaj niveloj kun rezervaj spuriloj.
- [`aggressive`](../../lists/transmission/aggressive.txt): provizora uzo por raraj aŭ malfortaj svarmoj.
- [`all`](../../lists/transmission/all.txt): ĉiuj nun kontrolitaj UDP-, HTTP- kaj HTTPS-spuriloj.
- [`candidates`](../../lists/candidates/all.txt): la plena inventaro, ankaŭ kun nun neatingeblaj adresoj.

Aldoni spurilojn al Magnet-ligilo:

```bash
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
```

Privataj spuriloj kun persona passkey ne estas publikigataj. “Alive” nur signifas validan respondon dum la plej lasta kontrolo; ĝi ne garantias samtavolanojn aŭ kompletan fonton por specifa torento.
