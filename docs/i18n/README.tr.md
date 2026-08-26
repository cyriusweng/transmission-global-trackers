# Transmission için küresel Tracker koleksiyonu

[English](../../README.md) · [简体中文](../../README.zh-CN.md)

Proje birçok açık kaynaktan genel BitTorrent Tracker adreslerini toplar, kaynak bilgisini korur, her gün doğrular ve Transmission 4.1+, diğer BitTorrent istemcileri, WebTorrent ve özel ağlar için anlaşılır listeler üretir.

## Doğru listeyi seçin

| Liste | Kullanım |
| --- | --- |
| [`macos.txt`](../../lists/transmission/macos.txt) | macOS Transmission arayüzü; seçilmiş 12 ana Tracker. |
| [`magnet.txt`](../../lists/transmission/magnet.txt) | Magnet URI'ye eklenecek 12 Tracker; bağlantıyı gereksiz büyütmez. |
| [`balanced.txt`](../../lists/transmission/balanced.txt) | daemon/RPC `default_trackers`; her birinde iki yedek bulunan 12 paralel katman. |
| [`aggressive.txt`](../../lists/transmission/aggressive.txt) | Nadir veya zayıf swarm için geçici; en fazla 60 host. |
| [`all.txt`](../../lists/transmission/all.txt) | Şu anda doğrulanmış tüm UDP, HTTP ve HTTPS Tracker'lar. |
| [`candidates/all.txt`](../../lists/candidates/all.txt) | Çevrimdışı adresler dâhil tam envanter; günlük liste olarak içe aktarmayın. |
| [`webtorrent/all.txt`](../../lists/webtorrent/all.txt) | WebTorrent WS/WSS; Transmission desteklemez. |
| [`special/`](../../lists/special/) | I2P/Yggdrasil yalnızca ilgili ağ yolu yapılandırılmışsa. |

## Transmission macOS'a Tracker ekleme

1. [`macos.txt`](../../lists/transmission/macos.txt) dosyasını açıp 12 satırı kopyalayın.
2. Transmission'da yalnızca bir aktarım seçin.
3. **View → Show Inspector** ve ardından **Trackers** sekmesini açın.
4. **+** düğmesine basın, satırları yeni alana yapıştırıp onaylayın.
5. Her satır bağımsız bir katman olur. Announce ve peer discovery için birkaç dakika bekleyin.

Bu işlemde `macos.txt` kullanın. macOS arayüzüne `balanced.txt` yapıştırmak yedek katman yapısını düzleştirir. Private torrent'ler çoğunlukla DHT, PeX ve dış Tracker'ları yasaklar; site kurallarına uyun.

## Magnet bağlantısını güçlendirme

```bash
git clone https://github.com/cyriusweng/transmission-global-trackers.git
cd transmission-global-trackers
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
python3 scripts/boost_magnet.py --profile balanced --open 'magnet:?xt=urn:btih:...'
```

Komut yeni Magnet yazdırır. `balanced` 12 Tracker, `aggressive` en fazla 60, `all` ise tanılama için tüm doğrulanmış Tracker'ları ekler. Mevcut `tr=` parametreleri korunur ve tekrarlar silinir.

## Kalıcı varsayılan Tracker

`default_trackers` BEP 12'yi izler: tek satır sonu aynı katmanda yedek, boş satır yeni paralel katman demektir. daemon/RPC ile [`balanced.txt`](../../lists/transmission/balanced.txt) kullanın. Yerel macOS arayüzünde kalıcı genel alan yoktur; aktarım başına `macos.txt` ekleyin veya Magnet'i önce güçlendirin.

## Diğer istemciler

qBittorrent, Deluge ve BiglyBT [`best.txt`](../../lists/transmission/best.txt) ya da [`all.txt`](../../lists/transmission/all.txt) kullanabilir. aria2/Motrix `all.txt` veya gereken virgül biçimini kullanır. WebTorrent `webtorrent/all.txt` kullanır.

## Otomatik güncelleme

GitHub Actions her gün 03:17 UTC'de çalışır; bilgisayarınız kapalı olabilir. Bulut Runner toplar, hafif protokol kontrolü yapar, geçmişi günceller, testleri çalıştırır ve commit gönderir. Torrent içeriği indirilmez ve Runner peer olarak kaydolmaz. Ülke, ISP, VPN ve IPv6 sonuçları değiştirebilir.

## Sınırlar ve gizlilik

“Alive” yalnızca son kontrolde geçerli yanıtı gösterir; belirli infohash için peer veya tam seed garantisi vermez. Tracker, tüm swarm'da eksik veriyi üretemez. Büyük profiller infohash'i daha fazla operatöre gösterir. Kişisel passkey hesap kimlik bilgisidir ve dışarıda bırakılır.

Ek paket olmadan yerel yeniden üretim:

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests
```
