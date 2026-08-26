# Transmission 向けグローバル Tracker 集約

[English](../../README.md) · [简体中文](../../README.zh-CN.md)

複数の公開ソースから BitTorrent Tracker を収集し、重複を除去して毎日検証し、Transmission 4.1+ 向けに使いやすい階層構成を生成します。

- [`balanced`](../../lists/transmission/balanced.txt)：日常利用の推奨設定。少数の並列 Tier と予備 Tracker を組み合わせます。
- [`aggressive`](../../lists/transmission/aggressive.txt)：希少または弱い swarm に一時的に使用します。
- [`all`](../../lists/transmission/all.txt)：現在検証済みの UDP／HTTP／HTTPS Tracker 全件。
- [`candidates`](../../lists/candidates/all.txt)：現在到達できない項目も含む全候補。

Magnet リンクへ Tracker を追加する方法：

```bash
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
```

個人 passkey を含むプライベート Tracker は収録しません。「Alive」は直近の検査で正常な応答があったことだけを示し、特定 Torrent の peer や完全な seed を保証しません。
