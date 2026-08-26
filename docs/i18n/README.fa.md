<div dir="rtl">

# ردیاب‌های جهانی برای Transmission

[English](../../README.md) · [简体中文](../../README.zh-CN.md)

این پروژه ردیاب‌های عمومی BitTorrent را از چند منبع گردآوری می‌کند، نسبت منبع را نگه می‌دارد، هر روز آن‌ها را می‌آزماید و برای Transmission 4.1+، مشتری‌های معمول BitTorrent، WebTorrent و شبکه‌های ویژه فهرست‌های روشن می‌سازد.

## فهرست مناسب را انتخاب کنید

| فهرست | کاربرد |
| --- | --- |
| [`macos.txt`](../../lists/transmission/macos.txt) | رابط macOS برنامهٔ Transmission؛ ۱۲ ردیاب اصلی برگزیده. |
| [`magnet.txt`](../../lists/transmission/magnet.txt) | افزودن به Magnet URI بدون طولانی شدن بیش از حد پیوند. |
| [`balanced.txt`](../../lists/transmission/balanced.txt) | تنظیم `default_trackers` با daemon یا RPC؛ ۱۲ ردهٔ موازی با دو پشتیبان در هر رده. |
| [`aggressive.txt`](../../lists/transmission/aggressive.txt) | استفادهٔ موقت برای swarm کمیاب یا ضعیف؛ تا ۶۰ میزبان. |
| [`all.txt`](../../lists/transmission/all.txt) | همهٔ ردیاب‌های UDP، HTTP و HTTPS که اکنون تأیید شده‌اند. |
| [`candidates/all.txt`](../../lists/candidates/all.txt) | فهرست کامل، شامل نشانی‌های فعلاً خارج از دسترس؛ برای استفادهٔ روزمره وارد نکنید. |
| [`webtorrent/all.txt`](../../lists/webtorrent/all.txt) | WS/WSS برای WebTorrent؛ Transmission از آن‌ها پشتیبانی نمی‌کند. |
| [`special/`](../../lists/special/) | I2P/Yggdrasil فقط هنگامی که مسیر شبکه تنظیم شده باشد. |

## افزودن ردیاب در Transmission روی macOS

۱. [`macos.txt`](../../lists/transmission/macos.txt) را باز و هر ۱۲ خط را کپی کنید.
۲. در Transmission فقط یک انتقال را انتخاب کنید.
۳. **View → Show Inspector** و سپس زبانهٔ **Trackers** را باز کنید.
۴. دکمهٔ **+** را بزنید، خطوط را در فیلد جدید بچسبانید و تأیید کنید.
۵. هر خط به‌صورت یک ردهٔ مستقل افزوده می‌شود. چند دقیقه برای announce و یافتن peerها صبر کنید.

در این روش از `macos.txt` استفاده کنید؛ چسباندن `balanced.txt` در رابط macOS ساختار پشتیبان را از بین می‌برد. تورنت خصوصی معمولاً DHT، PeX و ردیاب خارجی را منع می‌کند؛ قوانین سایت را رعایت کنید.

## تقویت Magnet

```bash
git clone https://github.com/cyriusweng/transmission-global-trackers.git
cd transmission-global-trackers
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
python3 scripts/boost_magnet.py --profile balanced --open 'magnet:?xt=urn:btih:...'
```

فرمان یک Magnet جدید چاپ می‌کند. `balanced` دوازده ردیاب، `aggressive` تا ۶۰ و `all` همهٔ ردیاب‌های تأییدشده را برای عیب‌یابی اضافه می‌کند. پارامترهای `tr=` موجود حفظ و موارد تکراری حذف می‌شوند.

## ردیاب پیش‌فرض پایدار

`default_trackers` از BEP 12 پیروی می‌کند: یک خط جدید پشتیبان همان رده است و خط خالی ردهٔ موازی تازه‌ای می‌سازد. برای daemon یا RPC از [`balanced.txt`](../../lists/transmission/balanced.txt) استفاده کنید. رابط اصلی macOS فیلد سراسری پایدار ندارد؛ برای هر کار `macos.txt` را به‌کار ببرید یا Magnet را تقویت کنید.

## مشتری‌های دیگر

qBittorrent، Deluge و BiglyBT می‌توانند [`best.txt`](../../lists/transmission/best.txt) یا [`all.txt`](../../lists/transmission/all.txt) را استفاده کنند. aria2 و Motrix از `all.txt` یا قالب جداشده با ویرگول استفاده می‌کنند. WebTorrent از `webtorrent/all.txt` استفاده می‌کند.

## به‌روزرسانی خودکار

GitHub Actions هر روز ساعت 03:17 UTC اجرا می‌شود و رایانهٔ شما می‌تواند خاموش باشد. Runner گردآوری، بررسی سبک پروتکل، به‌روزرسانی سابقه، آزمون و commit را انجام می‌دهد. محتوای Torrent دانلود نمی‌شود و Runner به‌عنوان peer ثبت نمی‌شود. نتیجه با کشور، ISP، VPN و IPv6 تفاوت دارد.

## محدودیت و حریم خصوصی

«Alive» فقط پاسخ معتبر در آخرین بررسی است و peer یا seed کامل برای infohash را تضمین نمی‌کند. ردیاب داده‌ای را که در کل swarm وجود ندارد بازسازی نمی‌کند. فهرست بزرگ infohash را به گردانندگان بیشتری نشان می‌دهد. passkey شخصی اعتبار حساب است و حذف می‌شود.

بازسازی محلی بدون بستهٔ اضافی:

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests
```

</div>
