# Transmission 全球 Tracker 聚合庫

[English](../../README.md) · [简体中文](../../README.zh-CN.md)

本專案從多個公開來源彙整 BitTorrent Tracker，保留來源、每日驗證，並為 Transmission 4.1+、其他傳統 BT 客戶端、WebTorrent 與專用網路產生可直接使用的分類清單。

## 選擇正確的清單

| 清單 | 適用情況 |
| --- | --- |
| [`macos.txt`](../../lists/transmission/macos.txt) | Transmission macOS 圖形介面；12 個精選主 Tracker。 |
| [`magnet.txt`](../../lists/transmission/magnet.txt) | 要附加到 Magnet URI；同一組 12 個主 Tracker。 |
| [`balanced.txt`](../../lists/transmission/balanced.txt) | 可透過 daemon 或 RPC 設定 `default_trackers`；12 個並行層，每層 2 個備援。 |
| [`aggressive.txt`](../../lists/transmission/aggressive.txt) | 稀有或弱 swarm 暫時使用，最多 60 個獨立主機。 |
| [`all.txt`](../../lists/transmission/all.txt) | 所有目前已驗證的 UDP／HTTP／HTTPS Tracker。 |
| [`candidates/all.txt`](../../lists/candidates/all.txt) | 完整候選，包含目前離線項目；不要當作日常匯入清單。 |
| [`webtorrent/all.txt`](../../lists/webtorrent/all.txt) | WS／WSS WebTorrent Tracker；Transmission 不支援。 |
| [`special/`](../../lists/special/) | I2P／Yggdrasil；只在相應網路已設定時使用。 |

## Transmission macOS：加入既有任務

1. 開啟 [`macos.txt`](../../lists/transmission/macos.txt)，複製全部 12 行。
2. 在 Transmission 中只選取一個任務。
3. 選擇 **View → Show Inspector**，開啟 **Trackers** 分頁。
4. 按 **+**，把多行內容貼入新 Tracker 欄位並確認。
5. 每一行會成為獨立 Tier；等待數分鐘完成 announce 與 peer discovery。

此流程請使用 `macos.txt`。macOS 介面貼上 `balanced.txt` 時會把備援層級攤平。私有 Torrent 通常禁止 DHT、PeX 與外部 Tracker，站規未明確允許時不要加入公開 Tracker。

## 增強 Magnet

```bash
git clone https://github.com/cyriusweng/transmission-global-trackers.git
cd transmission-global-trackers
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
python3 scripts/boost_magnet.py --profile balanced --open 'magnet:?xt=urn:btih:...'
```

指令會輸出新的 Magnet。`balanced` 加入 12 條；`aggressive` 最多 60 條；`all` 加入全部已驗證項目，只建議排障。既有 `tr=` 參數會保留並去重。

## 持久預設 Tracker

Transmission 的 `default_trackers` 遵循 BEP 12：單一換行表示同 Tier 備援，空白行表示新的並行 Tier。daemon 或 RPC 可直接使用 [`balanced.txt`](../../lists/transmission/balanced.txt)。原生 macOS 介面沒有全域持久輸入欄，請逐任務使用 `macos.txt` 或先增強 Magnet。

## 其他客戶端

qBittorrent、Deluge、BiglyBT 可從 [`best.txt`](../../lists/transmission/best.txt) 或 [`all.txt`](../../lists/transmission/all.txt) 開始；aria2／Motrix 使用 `all.txt` 或轉成應用要求的逗號格式；WebTorrent 使用 `webtorrent/all.txt`。

## 每日更新與驗證

GitHub Actions 每天 03:17 UTC 自動執行；你的電腦可以關機。Runner 會聚合來源、執行一次輕量協定握手、更新歷史排名、測試並提交。它不下載正文，也不把 Runner 登記為 peer。雲端結果不一定等同於所有國家、ISP、VPN 或 IPv6 路徑。

## 限制與隱私

「Alive」只代表最近檢查時有合法回應，不保證特定 infohash 有 peer 或完整 seed。更多 Tracker 無法補出整個 swarm 都缺少的資料。大量並行 Tracker 會向更多營運者暴露 infohash。含個人 passkey 的私有 Tracker 屬於帳戶憑證，因此不公開。

本機重建只需 Python 標準庫：

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests
```
