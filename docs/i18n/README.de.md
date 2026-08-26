# Globale Tracker für Transmission

[English](../../README.md) · [简体中文](../../README.zh-CN.md)

Das Projekt sammelt öffentliche BitTorrent-Tracker aus mehreren Quellen, bewahrt die Quellenangaben, prüft die Endpunkte täglich und erzeugt verständliche Listen für Transmission 4.1+, andere BitTorrent-Clients, WebTorrent und Spezialnetze.

## Die passende Liste wählen

| Liste | Verwendung |
| --- | --- |
| [`macos.txt`](../../lists/transmission/macos.txt) | Transmission-Oberfläche unter macOS; 12 ausgewählte Haupt-Tracker. |
| [`magnet.txt`](../../lists/transmission/magnet.txt) | Tracker an einen Magnet-Link anhängen, ohne ihn unnötig groß zu machen. |
| [`balanced.txt`](../../lists/transmission/balanced.txt) | `default_trackers` über Daemon oder RPC; 12 parallele Tiers mit je zwei Ausweich-Trackern. |
| [`aggressive.txt`](../../lists/transmission/aggressive.txt) | Vorübergehend für seltene oder schwache Schwärme; bis zu 60 Hosts. |
| [`all.txt`](../../lists/transmission/all.txt) | Alle derzeit bestätigten UDP-, HTTP- und HTTPS-Tracker. |
| [`candidates/all.txt`](../../lists/candidates/all.txt) | Vollständiger Bestand einschließlich momentan unerreichbarer Endpunkte; nicht als tägliche Liste importieren. |
| [`webtorrent/all.txt`](../../lists/webtorrent/all.txt) | WS/WSS für WebTorrent; Transmission unterstützt diese Protokolle nicht. |
| [`special/`](../../lists/special/) | I2P/Yggdrasil, nur mit eingerichteter Spezialroute. |

## Transmission unter macOS: Tracker hinzufügen

1. Öffnen Sie [`macos.txt`](../../lists/transmission/macos.txt) und kopieren Sie alle 12 Zeilen.
2. Wählen Sie in Transmission genau einen Transfer aus.
3. Öffnen Sie **View → Show Inspector** und den Reiter **Trackers**.
4. Klicken Sie auf **+**, fügen Sie die Zeilen in das neue Feld ein und bestätigen Sie.
5. Jede Zeile wird als eigenes Tier angelegt. Warten Sie einige Minuten auf Announce und Peer-Suche.

Verwenden Sie hierfür `macos.txt`. Beim Einfügen von `balanced.txt` geht die Ausweichstruktur in der macOS-Oberfläche verloren. Private Torrents untersagen meist DHT, PeX und fremde Tracker; fügen Sie öffentliche Tracker nur bei ausdrücklicher Erlaubnis hinzu.

## Einen Magnet-Link erweitern

```bash
git clone https://github.com/cyriusweng/transmission-global-trackers.git
cd transmission-global-trackers
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
python3 scripts/boost_magnet.py --profile balanced --open 'magnet:?xt=urn:btih:...'
```

Die Ausgabe ist ein neuer Magnet-Link. `balanced` fügt 12 Tracker hinzu, `aggressive` bis zu 60 und `all` sämtliche bestätigten Tracker für Diagnosezwecke. Vorhandene `tr=`-Parameter bleiben erhalten, Duplikate werden entfernt.

## Dauerhafte Standard-Tracker

`default_trackers` folgt BEP 12: ein Zeilenumbruch bedeutet Ausweich-Tracker im selben Tier, eine Leerzeile ein zusätzliches paralleles Tier. Verwenden Sie [`balanced.txt`](../../lists/transmission/balanced.txt) mit Daemon oder RPC. Die native macOS-Oberfläche bietet kein dauerhaftes globales Feld; nutzen Sie `macos.txt` je Transfer oder erweitern Sie den Magnet-Link.

## Andere Clients

qBittorrent, Deluge und BiglyBT können mit [`best.txt`](../../lists/transmission/best.txt) oder [`all.txt`](../../lists/transmission/all.txt) beginnen. aria2 und Motrix verwenden `all.txt` oder das benötigte Kommaformat. WebTorrent verwendet `webtorrent/all.txt`.

## Automatische Aktualisierung

GitHub Actions aktualisiert täglich um 03:17 UTC; der eigene Rechner kann ausgeschaltet sein. Der Runner aggregiert, prüft jeden Endpunkt einmal leichtgewichtig, aktualisiert den Verlauf, testet und committet Änderungen. Es werden keine Torrent-Daten geladen und der Runner registriert sich nicht als Peer. Ergebnisse können je nach Land, Provider, VPN oder IPv6 abweichen.

## Grenzen und Datenschutz

„Alive“ bestätigt nur eine gültige Antwort bei der letzten Prüfung; Peers oder ein vollständiger Seeder für einen Infohash sind damit nicht garantiert. Tracker ersetzen keine im gesamten Schwarm fehlenden Daten. Große Profile legen den Infohash mehr Betreibern offen. Persönliche Passkeys privater Tracker werden als Zugangsdaten ausgeschlossen.

Lokaler Neuaufbau ohne Zusatzpakete:

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests
```
