# Transmission 全球 Tracker 聚合库

**语言：** [English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](docs/i18n/README.zh-TW.md) · [Español](docs/i18n/README.es.md) · [Français](docs/i18n/README.fr.md) · [Deutsch](docs/i18n/README.de.md) · [Português](docs/i18n/README.pt-BR.md) · [Русский](docs/i18n/README.ru.md) · [日本語](docs/i18n/README.ja.md) · [한국어](docs/i18n/README.ko.md) · [العربية](docs/i18n/README.ar.md) · [فارسی](docs/i18n/README.fa.md) · [हिन्दी](docs/i18n/README.hi.md) · [Bahasa Indonesia](docs/i18n/README.id.md) · [Türkçe](docs/i18n/README.tr.md) · [Tiếng Việt](docs/i18n/README.vi.md) · [Українська](docs/i18n/README.uk.md) · [Esperanto](docs/i18n/README.eo.md) · [Íslenska](docs/i18n/README.is.md) · [Euskara](docs/i18n/README.eu.md) · [Cymraeg](docs/i18n/README.cy.md)

这是一个面向 Transmission 4.1+ 的全量公开 BitTorrent Tracker 聚合、验证和排布项目。它保留所有来源候选，同时为日常下载、稀有资源和排障分别生成适合的列表。

## 主要入口

| 列表 | 用途 |
| --- | --- |
| [`balanced.txt`](lists/transmission/balanced.txt) | 默认推荐。约 12 个并行层，每层带备用 Tracker，兼顾发现能力、请求量和响应速度。 |
| [`aggressive.txt`](lists/transmission/aggressive.txt) | 稀有资源或弱资源群临时使用，查询更多独立 Tracker 层。 |
| [`all-tiered.txt`](lists/transmission/all-tiered.txt) | 所有当前已验证且兼容 Transmission 的 Tracker，每条作为独立层；仅建议排障使用。 |
| [`all.txt`](lists/transmission/all.txt) | 所有当前已验证的 UDP、HTTP 和 HTTPS Tracker，每行一条。 |
| [`candidates/all.txt`](lists/candidates/all.txt) | 全量去重候选，包括当前离线项。 |
| [`webtorrent/all.txt`](lists/webtorrent/all.txt) | 已验证的 WS／WSS Tracker；Transmission 不支持这两种协议。 |
| [`special/`](lists/special/) | I2P／Yggdrasil 候选；普通 GitHub Runner 无法验证这些专用网络。 |
| [`status.csv`](data/status.csv) | 状态、延迟、排名、来源和诊断信息。 |

带个人 passkey 的私有站 Tracker 不会收录。passkey 属于账户凭证，公开发布既不安全，也无法供其他用户复用。

## 排布策略

Transmission 按 [BEP 12](https://www.bittorrent.org/beps/bep_0012.html) 解释 Tracker 层级：

- 单个换行：同一层内的备用 Tracker；
- 一个空行：新增一个并行查询层。

`balanced` 使用少量并行主层，并把额外端点放入备用位置。排名综合当前可达性、历史成功率、响应延迟、协议、主机去重和交叉来源数量。这样既保留全球覆盖，也避免每次添加 Torrent 都同时请求数百个服务器。完整算法见 [`docs/ALGORITHM.md`](docs/ALGORITHM.md)。

疑似断种资源可以临时使用 `aggressive`。完成元数据和节点发现后，恢复 `balanced` 更适合日常使用。任何 Tracker 列表都无法补出资源群中不存在的完整数据。

## 为 Magnet 附加 Tracker

```bash
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
```

可选配置为 `balanced`、`aggressive` 和 `all`。

## 本地更新

项目只使用 Python 标准库：

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests
```

GitHub Actions 每天自动更新。每个端点只接受一次轻量协议握手，不下载正文，也不向资源群登记节点。

## 来源与许可

[`sources.json`](sources.json) 记录完整来源、地址和来源许可；生成报告保留每条 Tracker 的来源归属。项目代码采用 GPL-3.0-or-later。

## 结果边界

「Alive」表示该端点在最近一次检查中返回了符合协议的响应。它不代表某个信息哈希一定有节点，也不代表节点持有完整资源；不同国家、运营商和代理路径的可达性仍可能不同。
