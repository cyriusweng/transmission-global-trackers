# Transmission के लिए वैश्विक Tracker संग्रह

[English](../../README.md) · [简体中文](../../README.zh-CN.md)

यह परियोजना कई सार्वजनिक स्रोतों से BitTorrent Tracker एकत्र करती है, स्रोत की जानकारी सुरक्षित रखती है, प्रतिदिन जाँच करती है और Transmission 4.1+, अन्य BitTorrent क्लाइंट, WebTorrent तथा विशेष नेटवर्क के लिए साफ़ उपयोग-सूचियाँ बनाती है।

## सही सूची चुनें

| सूची | उपयोग |
| --- | --- |
| [`macos.txt`](../../lists/transmission/macos.txt) | Transmission macOS GUI के लिए चुने गए 12 मुख्य Tracker। |
| [`magnet.txt`](../../lists/transmission/magnet.txt) | Magnet URI में जोड़ने के लिए वही 12 Tracker। |
| [`balanced.txt`](../../lists/transmission/balanced.txt) | daemon/RPC के `default_trackers` के लिए; 12 समानांतर tier, हर tier में दो backup। |
| [`aggressive.txt`](../../lists/transmission/aggressive.txt) | दुर्लभ या कमजोर swarm के लिए अस्थायी उपयोग; अधिकतम 60 host। |
| [`all.txt`](../../lists/transmission/all.txt) | वर्तमान में सत्यापित सभी UDP, HTTP और HTTPS Tracker। |
| [`candidates/all.txt`](../../lists/candidates/all.txt) | अभी offline endpoint सहित पूरा संग्रह; इसे दैनिक सूची की तरह import न करें। |
| [`webtorrent/all.txt`](../../lists/webtorrent/all.txt) | WebTorrent के WS/WSS; Transmission इन्हें समर्थन नहीं देता। |
| [`special/`](../../lists/special/) | I2P/Yggdrasil route सेट होने पर ही। |

## Transmission macOS में Tracker जोड़ना

1. [`macos.txt`](../../lists/transmission/macos.txt) खोलकर सभी 12 पंक्तियाँ कॉपी करें।
2. Transmission में केवल एक transfer चुनें।
3. **View → Show Inspector** खोलें और **Trackers** tab चुनें।
4. **+** दबाएँ, नई field में पंक्तियाँ paste करें और पुष्टि करें।
5. हर पंक्ति स्वतंत्र tier बनेगी। announce और peer discovery के लिए कुछ मिनट दें।

इस तरीके में `macos.txt` उपयोग करें। macOS GUI में `balanced.txt` paste करने पर backup tier संरचना खत्म हो जाती है। private torrent प्रायः DHT, PeX और बाहरी Tracker रोकते हैं; site के नियम मानें।

## Magnet को मजबूत करना

```bash
git clone https://github.com/cyriusweng/transmission-global-trackers.git
cd transmission-global-trackers
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
python3 scripts/boost_magnet.py --profile balanced --open 'magnet:?xt=urn:btih:...'
```

कमांड नया Magnet प्रिंट करता है। `balanced` 12 Tracker जोड़ता है, `aggressive` अधिकतम 60 और `all` सभी सत्यापित Tracker जोड़ता है; `all` केवल जाँच के लिए है। पुराने `tr=` parameter सुरक्षित रहते हैं और duplicate हटते हैं।

## स्थायी default Tracker

`default_trackers` BEP 12 मानता है: एक newline उसी tier का backup है और blank line नया parallel tier बनाती है। daemon/RPC में [`balanced.txt`](../../lists/transmission/balanced.txt) लगाएँ। native macOS GUI में स्थायी global field नहीं है; हर transfer पर `macos.txt` लगाएँ या Magnet पहले boost करें।

## अन्य क्लाइंट

qBittorrent, Deluge और BiglyBT [`best.txt`](../../lists/transmission/best.txt) या [`all.txt`](../../lists/transmission/all.txt) उपयोग कर सकते हैं। aria2/Motrix `all.txt` या आवश्यक comma format लेते हैं। WebTorrent `webtorrent/all.txt` उपयोग करता है।

## स्वचालित दैनिक अपडेट

GitHub Actions रोज़ 03:17 UTC पर चलता है; आपका कंप्यूटर बंद रह सकता है। cloud Runner संग्रह, हल्की protocol जाँच, history update, tests और commit करता है। वह Torrent data डाउनलोड नहीं करता और peer के रूप में register नहीं होता। देश, ISP, VPN और IPv6 के अनुसार पहुँच अलग हो सकती है।

## सीमा और गोपनीयता

“Alive” केवल पिछली जाँच में सही उत्तर का संकेत है; किसी infohash के peer या पूर्ण seed की गारंटी नहीं। swarm में मौजूद ही नहीं डेटा को Tracker वापस नहीं ला सकता। बड़ी सूची infohash को अधिक operators तक भेजती है। निजी passkey account credential है, इसलिए शामिल नहीं होती।

बिना अतिरिक्त package स्थानीय rebuild:

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests
```
