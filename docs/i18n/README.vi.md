# Bộ Tracker toàn cầu cho Transmission

[English](../../README.md)

Dự án tổng hợp Tracker BitTorrent công khai từ nhiều nguồn, loại bỏ bản trùng, kiểm tra hằng ngày và tạo cách sắp xếp tối ưu cho Transmission 4.1+.

- [`balanced`](../../lists/transmission/balanced.txt): khuyến nghị cho sử dụng hằng ngày; một số tier chạy song song kèm Tracker dự phòng.
- [`aggressive`](../../lists/transmission/aggressive.txt): dùng tạm thời cho swarm hiếm hoặc yếu.
- [`all`](../../lists/transmission/all.txt): toàn bộ Tracker UDP, HTTP và HTTPS đang được xác minh.
- [`candidates`](../../lists/candidates/all.txt): danh mục đầy đủ, kể cả endpoint hiện không truy cập được.

Thêm Tracker vào liên kết Magnet:

```bash
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
```

Tracker riêng tư có passkey cá nhân không được thu thập. “Alive” chỉ cho biết endpoint đã trả lời đúng giao thức trong lần kiểm tra gần nhất; trạng thái này không bảo đảm Torrent cụ thể có peer hoặc seed đầy đủ.
