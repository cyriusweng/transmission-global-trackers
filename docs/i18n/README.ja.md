# Transmission 向けグローバル Tracker 集約

[English](../../README.md) · [简体中文](../../README.zh-CN.md)

複数の公開ソースから BitTorrent Tracker を収集し、出典を保持して毎日検証します。Transmission 4.1+、一般的な BitTorrent クライアント、WebTorrent、専用ネットワーク向けに用途別リストを生成します。

## リストの選び方

| リスト | 用途 |
| --- | --- |
| [`macos.txt`](../../lists/transmission/macos.txt) | Transmission の macOS GUI 用。厳選した主 Tracker 12 件。 |
| [`magnet.txt`](../../lists/transmission/magnet.txt) | Magnet URI に追加する 12 件。リンクの肥大化を防ぎます。 |
| [`balanced.txt`](../../lists/transmission/balanced.txt) | daemon／RPC の `default_trackers` 用。12 の並列 Tier と各 Tier 2 件の予備。 |
| [`aggressive.txt`](../../lists/transmission/aggressive.txt) | 希少・弱い swarm に一時利用。最大 60 ホスト。 |
| [`all.txt`](../../lists/transmission/all.txt) | 現在検証済みの UDP／HTTP／HTTPS Tracker 全件。 |
| [`candidates/all.txt`](../../lists/candidates/all.txt) | 現在到達不能な項目も含む全候補。日常リストとしては取り込まないでください。 |
| [`webtorrent/all.txt`](../../lists/webtorrent/all.txt) | WebTorrent 用 WS／WSS。Transmission は非対応です。 |
| [`special/`](../../lists/special/) | I2P／Yggdrasil の経路を設定済みの場合のみ使用。 |

## Transmission macOS：既存タスクへ追加

1. [`macos.txt`](../../lists/transmission/macos.txt) を開き、12 行すべてをコピーします。
2. Transmission でタスクを 1 件だけ選択します。
3. **View → Show Inspector** を開き、**Trackers** タブへ移動します。
4. **+** を押し、新しい欄に複数行を貼り付けて確定します。
5. 各行は独立 Tier として追加されます。announce と peer discovery に数分待ってください。

この手順では `macos.txt` を使います。macOS GUI に `balanced.txt` を貼ると予備 Tier 構造が失われます。private torrent は通常 DHT、PeX、外部 Tracker を禁止するため、サイト規則を優先してください。

## Magnet を強化する

```bash
git clone https://github.com/cyriusweng/transmission-global-trackers.git
cd transmission-global-trackers
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
python3 scripts/boost_magnet.py --profile balanced --open 'magnet:?xt=urn:btih:...'
```

新しい Magnet が出力されます。`balanced` は 12 件、`aggressive` は最大 60 件、`all` は検証済み全件で診断時のみ推奨します。既存の `tr=` は保持され、重複は削除されます。

## 永続的な既定 Tracker

`default_trackers` は BEP 12 に従います。1 回の改行は同じ Tier の予備、空行は新しい並列 Tier です。daemon／RPC では [`balanced.txt`](../../lists/transmission/balanced.txt) をそのまま使えます。macOS ネイティブ GUI には永続的な全体設定欄がないため、タスクごとに `macos.txt` を使うか Magnet を先に強化します。

## 他のクライアント

qBittorrent、Deluge、BiglyBT は [`best.txt`](../../lists/transmission/best.txt) または [`all.txt`](../../lists/transmission/all.txt) から始められます。aria2／Motrix は `all.txt` または必要なカンマ形式を使用します。WebTorrent は `webtorrent/all.txt` を使用します。

## 自動更新

GitHub Actions が毎日 03:17 UTC に実行されるため、自分の PC は電源オフでも構いません。クラウド Runner が集約、軽量なプロトコル確認、履歴更新、テスト、コミットを行います。Torrent 本文は取得せず、peer として登録しません。国、ISP、VPN、IPv6 により到達性は異なります。

## 制限とプライバシー

「Alive」は直近の検査で有効応答があったことだけを示し、特定 infohash の peer や完全 seed を保証しません。全 swarm にないデータは Tracker では復元できません。大きなプロファイルは infohash をより多くの運営者へ公開します。個人 passkey は認証情報なので除外します。

追加パッケージなしでローカル再生成できます：

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests
```
