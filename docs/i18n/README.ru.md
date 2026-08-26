# Глобальные трекеры для Transmission

[English](../../README.md) · [简体中文](../../README.zh-CN.md)

Проект собирает публичные BitTorrent-трекеры из нескольких источников, сохраняет атрибуцию, ежедневно проверяет адреса и создаёт понятные списки для Transmission 4.1+, других BitTorrent-клиентов, WebTorrent и специализированных сетей.

## Какой список выбрать

| Список | Назначение |
| --- | --- |
| [`macos.txt`](../../lists/transmission/macos.txt) | Интерфейс Transmission для macOS; 12 отобранных основных трекеров. |
| [`magnet.txt`](../../lists/transmission/magnet.txt) | Добавление трекеров в Magnet URI без чрезмерной длины ссылки. |
| [`balanced.txt`](../../lists/transmission/balanced.txt) | `default_trackers` через daemon или RPC; 12 параллельных уровней с двумя резервами в каждом. |
| [`aggressive.txt`](../../lists/transmission/aggressive.txt) | Временно для редких или слабых раздач; до 60 независимых хостов. |
| [`all.txt`](../../lists/transmission/all.txt) | Все подтверждённые сейчас UDP-, HTTP- и HTTPS-трекеры. |
| [`candidates/all.txt`](../../lists/candidates/all.txt) | Полный каталог, включая временно недоступные адреса; не импортируйте как повседневный список. |
| [`webtorrent/all.txt`](../../lists/webtorrent/all.txt) | WS/WSS для WebTorrent; Transmission их не поддерживает. |
| [`special/`](../../lists/special/) | I2P/Yggdrasil при настроенной соответствующей сети. |

## Transmission на macOS: добавить трекеры

1. Откройте [`macos.txt`](../../lists/transmission/macos.txt) и скопируйте все 12 строк.
2. Выберите в Transmission только одну передачу.
3. Откройте **View → Show Inspector**, затем вкладку **Trackers**.
4. Нажмите **+**, вставьте строки в новое поле и подтвердите.
5. Каждая строка станет отдельным уровнем. Подождите несколько минут, пока выполнятся announce и поиск пиров.

Для этого используйте `macos.txt`: вставка `balanced.txt` в интерфейсе macOS разрушает структуру резервных уровней. Приватные торренты обычно запрещают DHT, PeX и внешние трекеры; соблюдайте правила сайта.

## Усилить Magnet-ссылку

```bash
git clone https://github.com/cyriusweng/transmission-global-trackers.git
cd transmission-global-trackers
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
python3 scripts/boost_magnet.py --profile balanced --open 'magnet:?xt=urn:btih:...'
```

Команда выводит новую Magnet-ссылку. `balanced` добавляет 12 трекеров, `aggressive` — до 60, `all` — все подтверждённые и предназначен только для диагностики. Имеющиеся параметры `tr=` сохраняются, дубликаты удаляются.

## Постоянные трекеры по умолчанию

`default_trackers` следует BEP 12: одна новая строка означает резерв в том же уровне, пустая строка создаёт новый параллельный уровень. Для daemon или RPC используйте [`balanced.txt`](../../lists/transmission/balanced.txt). Нативный интерфейс macOS не имеет постоянного глобального поля; применяйте `macos.txt` к каждой передаче или заранее усиливайте Magnet.

## Другие клиенты

qBittorrent, Deluge и BiglyBT могут использовать [`best.txt`](../../lists/transmission/best.txt) или [`all.txt`](../../lists/transmission/all.txt). aria2 и Motrix используют `all.txt` либо требуемый формат с запятыми. WebTorrent использует `webtorrent/all.txt`.

## Автоматическое обновление

GitHub Actions запускается ежедневно в 03:17 UTC; ваш компьютер может быть выключен. Runner агрегирует источники, выполняет лёгкую проверку протокола, обновляет историю, запускает тесты и отправляет изменения. Данные торрентов не загружаются, Runner не регистрируется как пир. Доступность может различаться по странам, провайдерам, VPN и IPv6.

## Ограничения и конфиденциальность

«Alive» означает лишь корректный ответ при последней проверке; наличие пиров или полного сида для infohash не гарантируется. Трекеры не восстанавливают отсутствующие во всём swarm данные. Большие профили раскрывают infohash большему числу операторов. Личные passkey приватных трекеров исключены как учётные данные.

Локальная сборка без сторонних пакетов:

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests
```
