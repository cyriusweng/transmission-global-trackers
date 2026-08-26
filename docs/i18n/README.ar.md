<div dir="rtl">

# متتبعات عالمية لبرنامج Transmission

[English](../../README.md)

يجمع هذا المشروع متتبعات BitTorrent العامة من مصادر متعددة، ويحذف التكرارات، ويتحقق منها يومياً، ثم ينشئ ترتيبات محسّنة لبرنامج Transmission 4.1+.

- [`balanced`](../../lists/transmission/balanced.txt): الخيار الموصى به للاستخدام اليومي؛ عدد محدود من الطبقات المتوازية مع متتبعات احتياطية.
- [`aggressive`](../../lists/transmission/aggressive.txt): استخدام مؤقت للتورنتات النادرة أو الأسراب الضعيفة.
- [`all`](../../lists/transmission/all.txt): جميع متتبعات UDP وHTTP وHTTPS التي تم التحقق منها حالياً.
- [`candidates`](../../lists/candidates/all.txt): القائمة الكاملة، بما فيها العناوين غير المتاحة حالياً.

لإضافة المتتبعات إلى رابط Magnet:

```bash
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
```

تُستبعد المتتبعات الخاصة التي تحتوي على passkey شخصي. تعني حالة «Alive» أن الخادم أعاد استجابة صحيحة في آخر فحص فقط؛ ولا تضمن وجود أقران أو موزّع كامل لتورنت معيّن.

</div>
