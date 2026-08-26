# Глобальні трекери для Transmission

[English](../../README.md) · [简体中文](../../README.zh-CN.md)

Проєкт збирає публічні BitTorrent-трекери з кількох джерел, зберігає атрибуцію, щодня перевіряє адреси та створює зрозумілі списки для Transmission 4.1+, інших BitTorrent-клієнтів, WebTorrent і спеціалізованих мереж.

## Оберіть правильний список

| Список | Використання |
| --- | --- |
| [`macos.txt`](../../lists/transmission/macos.txt) | Інтерфейс Transmission на macOS; 12 відібраних основних трекерів. |
| [`magnet.txt`](../../lists/transmission/magnet.txt) | Додавання до Magnet URI без надмірної довжини посилання. |
| [`balanced.txt`](../../lists/transmission/balanced.txt) | `default_trackers` через daemon/RPC; 12 паралельних рівнів із двома резервами. |
| [`aggressive.txt`](../../lists/transmission/aggressive.txt) | Тимчасово для рідкісного або слабкого swarm; до 60 хостів. |
| [`all.txt`](../../lists/transmission/all.txt) | Усі перевірені зараз UDP-, HTTP- та HTTPS-трекери. |
| [`candidates/all.txt`](../../lists/candidates/all.txt) | Повний каталог, включно з недоступними адресами; не імпортуйте як щоденний список. |
| [`webtorrent/all.txt`](../../lists/webtorrent/all.txt) | WS/WSS для WebTorrent; Transmission їх не підтримує. |
| [`special/`](../../lists/special/) | I2P/Yggdrasil лише з налаштованим мережевим маршрутом. |

## Додати трекери в Transmission macOS

1. Відкрийте [`macos.txt`](../../lists/transmission/macos.txt) і скопіюйте всі 12 рядків.
2. Виберіть у Transmission лише одну передачу.
3. Відкрийте **View → Show Inspector**, потім вкладку **Trackers**.
4. Натисніть **+**, вставте рядки в нове поле й підтвердьте.
5. Кожен рядок стане окремим рівнем. Зачекайте кілька хвилин на announce та пошук пірів.

Для цього використовуйте `macos.txt`. Вставлення `balanced.txt` у macOS-інтерфейс руйнує структуру резервних рівнів. Приватні торенти зазвичай забороняють DHT, PeX і сторонні трекери; дотримуйтеся правил сайту.

## Посилити Magnet

```bash
git clone https://github.com/cyriusweng/transmission-global-trackers.git
cd transmission-global-trackers
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
python3 scripts/boost_magnet.py --profile balanced --open 'magnet:?xt=urn:btih:...'
```

Команда друкує новий Magnet. `balanced` додає 12 трекерів, `aggressive` — до 60, `all` — усі перевірені лише для діагностики. Наявні параметри `tr=` зберігаються, дублікати видаляються.

## Постійні трекери за замовчуванням

`default_trackers` дотримується BEP 12: один перенос рядка означає резерв у тому самому рівні, порожній рядок створює новий паралельний рівень. Для daemon/RPC використовуйте [`balanced.txt`](../../lists/transmission/balanced.txt). Нативний інтерфейс macOS не має постійного глобального поля; додавайте `macos.txt` до кожної передачі або посилюйте Magnet заздалегідь.

## Інші клієнти

qBittorrent, Deluge і BiglyBT можуть використовувати [`best.txt`](../../lists/transmission/best.txt) або [`all.txt`](../../lists/transmission/all.txt). aria2/Motrix використовують `all.txt` чи потрібний формат із комами. WebTorrent використовує `webtorrent/all.txt`.

## Автоматичне оновлення

GitHub Actions запускається щодня о 03:17 UTC; ваш комп’ютер може бути вимкнений. Cloud Runner агрегує, робить легку перевірку протоколу, оновлює історію, запускає тести й надсилає commit. Дані Torrent не завантажуються, Runner не реєструється як peer. Результати можуть відрізнятися залежно від країни, провайдера, VPN та IPv6.

## Межі й приватність

«Alive» означає лише коректну відповідь під час останньої перевірки; це не гарантує пірів або повного сіда для infohash. Трекер не відновить дані, яких немає в усьому swarm. Великі профілі відкривають infohash більшій кількості операторів. Особисті passkey є обліковими даними й виключаються.

Локальна перебудова без додаткових пакетів:

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests
```
