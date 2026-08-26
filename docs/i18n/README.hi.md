# Transmission के लिए वैश्विक Tracker संग्रह

[English](../../README.md)

यह परियोजना कई सार्वजनिक स्रोतों से BitTorrent Tracker एकत्र करती है, डुप्लिकेट हटाती है, प्रतिदिन उनकी जाँच करती है और Transmission 4.1+ के लिए उपयोगी tier व्यवस्था बनाती है।

- [`balanced`](../../lists/transmission/balanced.txt): दैनिक उपयोग के लिए अनुशंसित; सीमित समानांतर tier और बैकअप Tracker।
- [`aggressive`](../../lists/transmission/aggressive.txt): दुर्लभ या कमजोर swarm के लिए अस्थायी विकल्प।
- [`all`](../../lists/transmission/all.txt): वर्तमान में सत्यापित सभी UDP, HTTP और HTTPS Tracker।
- [`candidates`](../../lists/candidates/all.txt): पूर्ण सूची, जिसमें अभी अनुपलब्ध endpoint भी शामिल हैं।

Magnet लिंक में Tracker जोड़ने के लिए:

```bash
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
```

व्यक्तिगत passkey वाले निजी Tracker शामिल नहीं किए जाते। “Alive” केवल अंतिम जाँच में वैध उत्तर मिलने का संकेत है; यह किसी विशेष Torrent के लिए peer या पूर्ण seed की गारंटी नहीं देता।
