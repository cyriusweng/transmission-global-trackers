<div dir="rtl">

# متتبعات عالمية لبرنامج Transmission

[English](../../README.md) · [简体中文](../../README.zh-CN.md)

يجمع المشروع متتبعات BitTorrent العامة من مصادر متعددة مع حفظ نسب المصدر، ويفحصها يومياً، ثم ينشئ قوائم واضحة لـ Transmission 4.1+ والعملاء التقليديين وWebTorrent والشبكات المتخصصة.

## اختر القائمة المناسبة

| القائمة | الاستخدام |
| --- | --- |
| [`macos.txt`](../../lists/transmission/macos.txt) | واجهة Transmission على macOS؛ أفضل 12 متتبعاً رئيسياً. |
| [`magnet.txt`](../../lists/transmission/magnet.txt) | لإضافتها إلى Magnet URI من دون تضخيم الرابط. |
| [`balanced.txt`](../../lists/transmission/balanced.txt) | لإعداد `default_trackers` عبر daemon أو RPC؛ 12 طبقة متوازية وفي كل طبقة بديلان. |
| [`aggressive.txt`](../../lists/transmission/aggressive.txt) | مؤقتاً للأسراب النادرة أو الضعيفة؛ حتى 60 مضيفاً. |
| [`all.txt`](../../lists/transmission/all.txt) | جميع متتبعات UDP وHTTP وHTTPS التي تم التحقق منها حالياً. |
| [`candidates/all.txt`](../../lists/candidates/all.txt) | الفهرس الكامل بما فيه العناوين غير المتاحة؛ لا تستورده كقائمة يومية. |
| [`webtorrent/all.txt`](../../lists/webtorrent/all.txt) | WS/WSS لـ WebTorrent؛ لا يدعمها Transmission. |
| [`special/`](../../lists/special/) | I2P/Yggdrasil عند إعداد مسار الشبكة المناسب فقط. |

## إضافة المتتبعات في Transmission على macOS

1. افتح [`macos.txt`](../../lists/transmission/macos.txt) وانسخ الأسطر الاثني عشر.
2. حدّد عملية نقل واحدة فقط في Transmission.
3. افتح **View → Show Inspector** ثم علامة **Trackers**.
4. اضغط **+**، والصق الأسطر في الحقل الجديد ثم أكّد.
5. يضيف Transmission كل سطر كطبقة مستقلة. انتظر بضع دقائق لإعلانات tracker واكتشاف الأقران.

استخدم `macos.txt` هنا؛ لصق `balanced.txt` في واجهة macOS يلغي بنية البدائل. التورنت الخاص يمنع عادة DHT وPeX والمتتبعات الخارجية، لذا التزم بقواعد الموقع.

## تعزيز رابط Magnet

```bash
git clone https://github.com/cyriusweng/transmission-global-trackers.git
cd transmission-global-trackers
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
python3 scripts/boost_magnet.py --profile balanced --open 'magnet:?xt=urn:btih:...'
```

يطبع الأمر Magnet جديداً. يضيف `balanced` اثني عشر متتبعاً، و`aggressive` حتى 60، و`all` جميع المتتبعات المتحققة للاختبار فقط. تُحفظ معاملات `tr=` الموجودة وتُزال التكرارات.

## المتتبعات الافتراضية الدائمة

يتبع `default_trackers` معيار BEP 12: سطر جديد يعني بديلاً في الطبقة نفسها، وسطر فارغ ينشئ طبقة متوازية جديدة. استخدم [`balanced.txt`](../../lists/transmission/balanced.txt) مع daemon أو RPC. واجهة macOS الأصلية لا تعرض حقلاً عالمياً دائماً؛ استخدم `macos.txt` لكل مهمة أو عزّز Magnet أولاً.

## عملاء آخرون

يمكن لـ qBittorrent وDeluge وBiglyBT استخدام [`best.txt`](../../lists/transmission/best.txt) أو [`all.txt`](../../lists/transmission/all.txt). يستخدم aria2 وMotrix ملف `all.txt` أو تنسيق الفواصل المطلوب. يستخدم WebTorrent ملف `webtorrent/all.txt`.

## التحديث التلقائي

تشغّل GitHub Actions التحديث يومياً عند 03:17 UTC، ولا يلزم تشغيل حاسوبك. يجمع Runner المصادر، وينفذ فحص بروتوكول خفيفاً، ويحدّث السجل، ويشغّل الاختبارات، ثم يرسل التغييرات. لا ينزّل محتوى Torrent ولا يسجل نفسه كقرين. قد تختلف النتائج حسب البلد ومزود الخدمة وVPN وIPv6.

## الحدود والخصوصية

تعني «Alive» استجابة صالحة في آخر فحص فقط؛ ولا تضمن أقراناً أو seed كاملاً لـ infohash معين. لا يعيد المتتبع بيانات مفقودة من كل أفراد السرب. القوائم الكبيرة تكشف infohash لمشغلين أكثر. تُستبعد passkey الشخصية لأنها بيانات اعتماد حساب.

إعادة البناء محلياً بلا حزم إضافية:

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests
```

</div>
