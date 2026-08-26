# Alþjóðlegt Tracker-safn fyrir Transmission

[English](../../README.md)

Verkefnið safnar opinberum BitTorrent Tracker-slóðum úr mörgum heimildum, fjarlægir tvítekningar, prófar þær daglega og býr til skipulag fyrir Transmission 4.1+.

- [`balanced`](../../lists/transmission/balanced.txt): ráðlagt í daglegri notkun; fá samhliða tier með vara-Trackerum.
- [`aggressive`](../../lists/transmission/aggressive.txt): tímabundið fyrir sjaldgæfa eða veika swarm-a.
- [`all`](../../lists/transmission/all.txt): allir UDP-, HTTP- og HTTPS-Trackerar sem standast nýjustu prófun.
- [`candidates`](../../lists/candidates/all.txt): allt safnið, einnig slóðir sem eru óaðgengilegar núna.

Bæta Trackerum við Magnet-slóð:

```bash
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
```

Einka-Trackerar með persónulegu passkey eru ekki birtir. „Alive“ staðfestir aðeins gilt svar í síðustu prófun og tryggir hvorki peer-a né fullan seed fyrir tiltekið Torrent.
