# Глобальні трекери для Transmission

[English](../../README.md)

Проєкт збирає публічні BitTorrent-трекери з кількох джерел, видаляє дублікати, щодня перевіряє доступність і створює оптимізовані списки для Transmission 4.1+.

- [`balanced`](../../lists/transmission/balanced.txt) — рекомендований щоденний профіль: кілька паралельних рівнів і резервні трекери.
- [`aggressive`](../../lists/transmission/aggressive.txt) — тимчасовий профіль для рідкісних або слабких роздач.
- [`all`](../../lists/transmission/all.txt) — усі перевірені зараз UDP-, HTTP- та HTTPS-трекери.
- [`candidates`](../../lists/candidates/all.txt) — повний перелік, включно з тимчасово недоступними адресами.

Додати трекери до Magnet-посилання:

```bash
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
```

Приватні трекери з особистими passkey не публікуються. Статус «Alive» означає лише коректну відповідь під час останньої перевірки й не гарантує наявності пірів або повного сіда для конкретного Torrent.
