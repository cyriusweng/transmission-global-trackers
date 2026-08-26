# Tracker global untuk Transmission

[English](../../README.md)

Proyek ini menggabungkan tracker BitTorrent publik dari banyak sumber, menghapus duplikasi, memeriksanya setiap hari, dan menghasilkan susunan yang dioptimalkan untuk Transmission 4.1+.

- [`balanced`](../../lists/transmission/balanced.txt): pilihan harian yang disarankan; beberapa tier paralel dengan tracker cadangan.
- [`aggressive`](../../lists/transmission/aggressive.txt): dipakai sementara untuk swarm langka atau lemah.
- [`all`](../../lists/transmission/all.txt): semua tracker UDP, HTTP, dan HTTPS yang saat ini terverifikasi.
- [`candidates`](../../lists/candidates/all.txt): inventaris lengkap, termasuk endpoint yang sedang tidak dapat dijangkau.

Menambahkan tracker ke tautan Magnet:

```bash
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
```

Tracker privat dengan passkey pribadi tidak disertakan. Status “Alive” hanya berarti endpoint memberi respons protokol yang sah pada pemeriksaan terakhir; status ini tidak menjamin peer atau seed lengkap untuk Torrent tertentu.
