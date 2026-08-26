# Bộ Tracker toàn cầu cho Transmission

[English](../../README.md) · [简体中文](../../README.zh-CN.md)

Dự án tổng hợp Tracker BitTorrent công khai từ nhiều nguồn, giữ thông tin nguồn, kiểm tra hằng ngày và tạo danh sách rõ ràng cho Transmission 4.1+, các ứng dụng BitTorrent khác, WebTorrent và mạng chuyên dụng.

## Chọn đúng danh sách

| Danh sách | Cách dùng |
| --- | --- |
| [`macos.txt`](../../lists/transmission/macos.txt) | Giao diện Transmission trên macOS; 12 Tracker chính được chọn. |
| [`magnet.txt`](../../lists/transmission/magnet.txt) | Gắn vào Magnet URI mà không làm liên kết quá dài. |
| [`balanced.txt`](../../lists/transmission/balanced.txt) | `default_trackers` qua daemon/RPC; 12 tier song song, mỗi tier có hai dự phòng. |
| [`aggressive.txt`](../../lists/transmission/aggressive.txt) | Tạm dùng cho swarm hiếm hoặc yếu; tối đa 60 host. |
| [`all.txt`](../../lists/transmission/all.txt) | Tất cả Tracker UDP, HTTP và HTTPS đang được xác minh. |
| [`candidates/all.txt`](../../lists/candidates/all.txt) | Toàn bộ ứng viên, kể cả endpoint đang offline; không nhập làm danh sách hằng ngày. |
| [`webtorrent/all.txt`](../../lists/webtorrent/all.txt) | WS/WSS cho WebTorrent; Transmission không hỗ trợ. |
| [`special/`](../../lists/special/) | I2P/Yggdrasil chỉ khi đã cấu hình đường mạng tương ứng. |

## Thêm Tracker trong Transmission macOS

1. Mở [`macos.txt`](../../lists/transmission/macos.txt) và sao chép cả 12 dòng.
2. Chỉ chọn một tác vụ trong Transmission.
3. Mở **View → Show Inspector**, rồi chọn tab **Trackers**.
4. Nhấn **+**, dán các dòng vào ô mới và xác nhận.
5. Mỗi dòng trở thành một tier độc lập. Chờ vài phút để announce và tìm peer.

Hãy dùng `macos.txt` cho cách này. Dán `balanced.txt` vào giao diện macOS sẽ làm mất cấu trúc dự phòng. Torrent riêng tư thường cấm DHT, PeX và Tracker bên ngoài; hãy tuân theo quy định của trang.

## Tăng cường Magnet

```bash
git clone https://github.com/cyriusweng/transmission-global-trackers.git
cd transmission-global-trackers
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
python3 scripts/boost_magnet.py --profile balanced --open 'magnet:?xt=urn:btih:...'
```

Lệnh in ra Magnet mới. `balanced` thêm 12 Tracker, `aggressive` tối đa 60, còn `all` thêm toàn bộ Tracker đã xác minh và chỉ nên dùng để chẩn đoán. Tham số `tr=` cũ được giữ lại và loại trùng.

## Tracker mặc định lâu dài

`default_trackers` theo BEP 12: một xuống dòng là Tracker dự phòng cùng tier, một dòng trống tạo tier song song mới. Dùng [`balanced.txt`](../../lists/transmission/balanced.txt) qua daemon/RPC. Giao diện macOS gốc không có ô mặc định toàn cục lâu dài; hãy dùng `macos.txt` cho từng tác vụ hoặc tăng cường Magnet trước.

## Ứng dụng khác

qBittorrent, Deluge và BiglyBT có thể dùng [`best.txt`](../../lists/transmission/best.txt) hoặc [`all.txt`](../../lists/transmission/all.txt). aria2/Motrix dùng `all.txt` hoặc định dạng dấu phẩy cần thiết. WebTorrent dùng `webtorrent/all.txt`.

## Cập nhật tự động

GitHub Actions chạy mỗi ngày lúc 03:17 UTC; máy tính của bạn có thể tắt. Runner đám mây tổng hợp, kiểm tra giao thức nhẹ, cập nhật lịch sử, chạy test và commit thay đổi. Nó không tải nội dung Torrent và không đăng ký làm peer. Kết quả có thể khác theo quốc gia, ISP, VPN và IPv6.

## Giới hạn và riêng tư

“Alive” chỉ xác nhận phản hồi hợp lệ ở lần kiểm tra gần nhất; không bảo đảm peer hoặc seed đầy đủ cho infohash. Tracker không thể tạo lại dữ liệu mà toàn swarm đều thiếu. Danh sách lớn làm lộ infohash cho nhiều nhà vận hành hơn. Passkey cá nhân là thông tin tài khoản nên bị loại.

Tạo lại cục bộ không cần gói ngoài:

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests
```
