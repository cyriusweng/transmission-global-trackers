# Transmission için küresel Tracker koleksiyonu

[English](../../README.md)

Bu proje birden fazla açık kaynaktan genel BitTorrent Tracker adreslerini toplar, tekrarları kaldırır, her gün doğrular ve Transmission 4.1+ için kullanışlı katman düzenleri üretir.

- [`balanced`](../../lists/transmission/balanced.txt): günlük kullanım için önerilir; az sayıda paralel katman ve yedek Tracker içerir.
- [`aggressive`](../../lists/transmission/aggressive.txt): nadir veya zayıf swarm'lar için geçici kullanım.
- [`all`](../../lists/transmission/all.txt): şu anda doğrulanmış tüm UDP, HTTP ve HTTPS Tracker'lar.
- [`candidates`](../../lists/candidates/all.txt): o anda çevrimdışı olan adresler dâhil tam envanter.

Magnet bağlantısına Tracker eklemek için:

```bash
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
```

Kişisel passkey içeren özel Tracker'lar yayımlanmaz. “Alive”, yalnızca son kontrolde geçerli yanıt alındığını gösterir; belirli bir Torrent için peer veya tam seed garantisi vermez.
