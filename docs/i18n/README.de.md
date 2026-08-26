# Globale Tracker für Transmission

[English](../../README.md)

Dieses Projekt sammelt öffentliche BitTorrent-Tracker aus mehreren Quellen, entfernt Duplikate, prüft sie täglich und erzeugt für Transmission 4.1+ optimierte Anordnungen.

- [`balanced`](../../lists/transmission/balanced.txt): empfohlene Alltagseinstellung mit wenigen parallelen Tiers und Ausweich-Trackern.
- [`aggressive`](../../lists/transmission/aggressive.txt): vorübergehend für seltene oder schwache Schwärme.
- [`all`](../../lists/transmission/all.txt): alle derzeit bestätigten UDP-, HTTP- und HTTPS-Tracker.
- [`candidates`](../../lists/candidates/all.txt): vollständiger Bestand einschließlich momentan nicht erreichbarer Endpunkte.

Tracker an einen Magnet-Link anhängen:

```bash
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
```

Private Tracker mit persönlichen Passkeys werden ausgeschlossen. „Alive“ bestätigt nur eine gültige Antwort bei der letzten Prüfung und garantiert weder Peers noch einen vollständigen Seeder für einen bestimmten Torrent.
