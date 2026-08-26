<div dir="rtl">

# ردیاب‌های جهانی برای Transmission

[English](../../README.md)

این پروژه ردیاب‌های عمومی BitTorrent را از چندین منبع گردآوری می‌کند، موارد تکراری را حذف می‌کند، هر روز آن‌ها را می‌آزماید و چیدمان‌های بهینه برای Transmission 4.1+ می‌سازد.

- [`balanced`](../../lists/transmission/balanced.txt): پیشنهاد روزمره؛ چند ردهٔ موازی همراه با ردیاب‌های پشتیبان.
- [`aggressive`](../../lists/transmission/aggressive.txt): استفادهٔ موقت برای swarmهای کمیاب یا ضعیف.
- [`all`](../../lists/transmission/all.txt): همهٔ ردیاب‌های UDP، HTTP و HTTPS که اکنون تأیید شده‌اند.
- [`candidates`](../../lists/candidates/all.txt): فهرست کامل، شامل نشانی‌های فعلاً خارج از دسترس.

افزودن ردیاب‌ها به پیوند Magnet:

```bash
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
```

ردیاب‌های خصوصی دارای passkey شخصی منتشر نمی‌شوند. وضعیت «Alive» فقط پاسخ معتبر در آخرین بررسی را نشان می‌دهد و وجود peer یا seed کامل برای یک تورنت خاص را تضمین نمی‌کند.

</div>
