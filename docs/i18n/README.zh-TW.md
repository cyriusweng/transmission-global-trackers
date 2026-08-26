# Transmission 全球 Tracker 聚合庫

[English](../../README.md) · [简体中文](../../README.zh-CN.md)

本專案從多個公開來源彙整 BitTorrent Tracker，去重後每天驗證，並為 Transmission 4.1+ 產生容易使用的層級配置。

- [`balanced`](../../lists/transmission/balanced.txt)：日常推薦；少量並行主層，每層附有備用 Tracker。
- [`aggressive`](../../lists/transmission/aggressive.txt)：稀有或弱資源群暫時使用。
- [`all`](../../lists/transmission/all.txt)：所有目前已驗證的 UDP／HTTP／HTTPS Tracker。
- [`candidates`](../../lists/candidates/all.txt)：完整候選，包括目前離線項目。

為 Magnet 加入 Tracker：

```bash
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
```

含個人 passkey 的私有 Tracker 不會公開收錄。「Alive」只代表最近檢查時端點回應正常，不保證特定資源一定有節點或完整做種者。
