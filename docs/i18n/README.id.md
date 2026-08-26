# Tracker global untuk Transmission

[English](../../README.md) · [简体中文](../../README.zh-CN.md)

Proyek ini menggabungkan tracker BitTorrent publik dari banyak sumber, mempertahankan atribusi, memeriksa endpoint setiap hari, lalu menghasilkan daftar yang jelas untuk Transmission 4.1+, klien BitTorrent lain, WebTorrent, dan jaringan khusus.

## Pilih daftar yang tepat

| Daftar | Penggunaan |
| --- | --- |
| [`macos.txt`](../../lists/transmission/macos.txt) | GUI Transmission di macOS; 12 tracker utama terpilih. |
| [`magnet.txt`](../../lists/transmission/magnet.txt) | Ditambahkan ke Magnet URI tanpa membuat tautan terlalu panjang. |
| [`balanced.txt`](../../lists/transmission/balanced.txt) | `default_trackers` melalui daemon/RPC; 12 tier paralel dengan dua cadangan per tier. |
| [`aggressive.txt`](../../lists/transmission/aggressive.txt) | Sementara untuk swarm langka atau lemah; hingga 60 host. |
| [`all.txt`](../../lists/transmission/all.txt) | Semua tracker UDP, HTTP, dan HTTPS yang saat ini terverifikasi. |
| [`candidates/all.txt`](../../lists/candidates/all.txt) | Inventaris lengkap termasuk endpoint yang sedang offline; jangan impor sebagai daftar harian. |
| [`webtorrent/all.txt`](../../lists/webtorrent/all.txt) | WS/WSS untuk WebTorrent; Transmission tidak mendukungnya. |
| [`special/`](../../lists/special/) | I2P/Yggdrasil hanya jika rute jaringan sudah tersedia. |

## Menambahkan tracker di Transmission macOS

1. Buka [`macos.txt`](../../lists/transmission/macos.txt) dan salin semua 12 baris.
2. Pilih tepat satu transfer di Transmission.
3. Buka **View → Show Inspector**, lalu tab **Trackers**.
4. Tekan **+**, tempel semua baris ke kolom baru, lalu konfirmasi.
5. Setiap baris menjadi tier terpisah. Tunggu beberapa menit untuk announce dan pencarian peer.

Gunakan `macos.txt` untuk langkah ini. Menempel `balanced.txt` di GUI macOS akan meratakan struktur cadangannya. Torrent privat biasanya melarang DHT, PeX, dan tracker luar; ikuti aturan situs.

## Memperkuat Magnet

```bash
git clone https://github.com/cyriusweng/transmission-global-trackers.git
cd transmission-global-trackers
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
python3 scripts/boost_magnet.py --profile balanced --open 'magnet:?xt=urn:btih:...'
```

Perintah mencetak Magnet baru. `balanced` menambah 12 tracker, `aggressive` hingga 60, dan `all` seluruh tracker terverifikasi untuk diagnosis saja. Parameter `tr=` lama dipertahankan dan duplikat dihapus.

## Tracker default yang persisten

`default_trackers` mengikuti BEP 12: satu baris baru berarti cadangan dalam tier yang sama, sedangkan baris kosong membuat tier paralel baru. Gunakan [`balanced.txt`](../../lists/transmission/balanced.txt) melalui daemon/RPC. GUI macOS asli tidak menyediakan kolom global persisten; gunakan `macos.txt` per transfer atau perkuat Magnet lebih dahulu.

## Klien lain

qBittorrent, Deluge, dan BiglyBT dapat memakai [`best.txt`](../../lists/transmission/best.txt) atau [`all.txt`](../../lists/transmission/all.txt). aria2/Motrix memakai `all.txt` atau format koma yang diminta. WebTorrent memakai `webtorrent/all.txt`.

## Pembaruan otomatis

GitHub Actions berjalan setiap hari pukul 03:17 UTC; komputer Anda boleh mati. Runner cloud mengagregasi, memeriksa protokol secara ringan, memperbarui riwayat, menjalankan tes, dan mengirim commit. Tidak ada isi Torrent yang diunduh dan Runner tidak mendaftarkan diri sebagai peer. Hasil dapat berbeda menurut negara, ISP, VPN, dan IPv6.

## Batas dan privasi

“Alive” hanya berarti respons valid pada pemeriksaan terakhir; tidak menjamin peer atau seed lengkap untuk suatu infohash. Tracker tidak dapat menciptakan data yang hilang dari seluruh swarm. Daftar besar mengungkap infohash kepada lebih banyak operator. Passkey privat adalah kredensial akun dan dikecualikan.

Bangun ulang lokal tanpa paket tambahan:

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests
```
