# Transmission 全球 Tracker 聚合库

**语言：** [English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](docs/i18n/README.zh-TW.md) · [Español](docs/i18n/README.es.md) · [Français](docs/i18n/README.fr.md) · [Deutsch](docs/i18n/README.de.md) · [Português](docs/i18n/README.pt-BR.md) · [Русский](docs/i18n/README.ru.md) · [日本語](docs/i18n/README.ja.md) · [한국어](docs/i18n/README.ko.md) · [العربية](docs/i18n/README.ar.md) · [فارسی](docs/i18n/README.fa.md) · [हिन्दी](docs/i18n/README.hi.md) · [Bahasa Indonesia](docs/i18n/README.id.md) · [Türkçe](docs/i18n/README.tr.md) · [Tiếng Việt](docs/i18n/README.vi.md) · [Українська](docs/i18n/README.uk.md) · [Esperanto](docs/i18n/README.eo.md) · [Íslenska](docs/i18n/README.is.md) · [Euskara](docs/i18n/README.eu.md) · [Cymraeg](docs/i18n/README.cy.md)

这是一个保留来源、持续验证的公开 BitTorrent Tracker 全量聚合项目。它既保存完整候选目录，也为 Transmission 4.1+、其他传统 BT 客户端、WebTorrent 和专用网络生成可以直接使用的分类列表。

## 先选对列表

| 列表 | 适用场景 |
| --- | --- |
| [`macos.txt`](lists/transmission/macos.txt) | 使用 Transmission macOS 图形界面。包含 12 个高排名主 Tracker，可以一次粘贴到单个任务。 |
| [`magnet.txt`](lists/transmission/magnet.txt) | 要为 Magnet 链接附加 Tracker。使用同一组 12 个主 Tracker，避免 Magnet 过长。 |
| [`balanced.txt`](lists/transmission/balanced.txt) | 能通过 daemon 配置或 RPC 设置 Transmission 的 `default_trackers`。包含 12 个并行层，每层有 2 个备用 Tracker。 |
| [`aggressive.txt`](lists/transmission/aggressive.txt) | 稀有资源几乎找不到节点。临时使用，最多查询 60 个独立 Tracker 主机。 |
| [`all.txt`](lists/transmission/all.txt) | 需要所有当前已验证的 UDP、HTTP 和 HTTPS Tracker，每行一条。 |
| [`all-tiered.txt`](lists/transmission/all-tiered.txt) | 正在排查弱资源群，并明确需要把所有已验证主机作为独立并行层。 |
| [`candidates/all.txt`](lists/candidates/all.txt) | 需要完整去重候选，包括当前离线项。不要把它当作日常列表直接导入客户端。 |
| [`webtorrent/all.txt`](lists/webtorrent/all.txt) | 使用支持 WS／WSS 的 WebTorrent 客户端。Transmission 不支持这两种协议。 |
| [`special/`](lists/special/) | 已配置 I2P 或 Yggdrasil 网络。普通 GitHub Runner 无法验证这些端点。 |
| [`status.csv`](data/status.csv) | 需要机器可读的状态、延迟、分数、来源和诊断细节。 |

## Transmission macOS：给现有任务添加 Tracker

1. 打开 [`macos.txt`](lists/transmission/macos.txt)，复制其中全部 12 行。
2. 在 Transmission 中只选中 **一个** 下载任务。
3. 选择 **View → Show Inspector**，然后打开 **Trackers** 标签页。
4. 点击 **+**，把刚才复制的多行内容粘贴到新 Tracker 输入框并确认。
5. Transmission 会把每一行作为独立 Tracker 层加入。等待几分钟，让客户端完成 announce 和节点发现。

这个流程应使用 `macos.txt`。macOS 图形界面粘贴 `balanced.txt` 时会把备用层级压平，因此不会比 12 条的 macOS 专用列表更有优势。

私有 Torrent 通常禁止 DHT、PeX 和外部 Tracker。除非私有站规则明确允许，否则不要向私有 Torrent 添加公开 Tracker。

## 给 Magnet 链接附加 Tracker

只需克隆一次仓库：

```bash
git clone https://github.com/cyriusweng/transmission-global-trackers.git
cd transmission-global-trackers
```

生成均衡版 Magnet：

```bash
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
python3 scripts/boost_magnet.py --profile balanced --open 'magnet:?xt=urn:btih:...'
```

第一条命令会输出一个新 Magnet，并附加 `magnet.txt` 中的 12 个 Tracker。第二条加入 `--open`，会在 macOS 上直接把结果交给 Transmission；之后是否显示确认窗口、是否立即开始，继续遵循你自己的 Transmission 偏好。可选配置：

- `balanced`：12 个主 Tracker，日常推荐；
- `aggressive`：最多 60 个 Tracker，给稀有资源临时使用；
- `all`：全部已验证且兼容 Transmission 的 Tracker，仅建议排障。

原链接已有的 `tr=` 参数会保留，重复项会自动删除。

## 持久化默认 Tracker

Transmission 的 `default_trackers` 遵循 [BEP 12](https://www.bittorrent.org/beps/bep_0012.html)：

- 单个换行表示同一层内的备用 Tracker；
- 一个空行表示新增一个并行查询层。

当 Transmission daemon、RPC 控制器或其他前端提供 `default_trackers` 设置时，直接使用 [`balanced.txt`](lists/transmission/balanced.txt) 的完整内容。原生 macOS 界面目前没有持久化全局默认 Tracker 输入框，因此应按任务使用 `macos.txt`，或先增强 Magnet 链接。

## 其他 BT 客户端也能用

这个仓库不限于 Transmission：

- **qBittorrent、Deluge、BiglyBT 等：** 先用 [`best.txt`](lists/transmission/best.txt) 或 [`all.txt`](lists/transmission/all.txt)，按客户端要求的格式导入。
- **aria2 和 Motrix：** 使用 [`all.txt`](lists/transmission/all.txt)，或转换成应用要求的逗号分隔格式。
- **WebTorrent：** 使用 [`webtorrent/all.txt`](lists/webtorrent/all.txt)。
- **I2P／Yggdrasil：** 只在对应网络已配置时使用 [`special/`](lists/special/) 中的文件。

UDP、HTTP 和 HTTPS 属于传统 BitTorrent Tracker 协议。WS／WSS 单独保存，因为常规 Transmission 不使用 WebTorrent Tracker。

## 列表怎样生成

每次计划任务都会：

1. 获取 [`sources.json`](sources.json) 中全部固定来源；
2. 提取并规范化 Tracker URL；
3. 全局去重，同时保留每条记录的全部来源和标签；
4. 对每个端点执行一次轻量协议检查；
5. 更新历史成功率和延迟；
6. 重新排名并生成所有用途列表。

UDP 使用 BEP 15 握手，HTTP／HTTPS 要求返回符合 Tracker 形态的 bencode 响应，WS／WSS 验证 WebSocket 升级。检测不会下载 Torrent 正文，也不会把 Runner 注册为资源群节点。完整算法见 [`docs/ALGORITHM.md`](docs/ALGORITHM.md)。

## 每日自动更新

GitHub Actions 每天 **03:17 UTC** 自动运行，北京时间约为 **11:17**。你的电脑无需开机。GitHub 托管的 Runner 会获取来源、验证、运行测试，并使用仓库自带的 `GITHUB_TOKEN` 自动提交变化。

也可以在仓库的 **Actions → Refresh tracker health → Run workflow** 手动触发。

检测结果代表 GitHub 云端 Runner 的网络可达性。不同国家、运营商、VPN 和 IPv6 路径可能得到不同结果。

## 准确性、隐私和边界

- 「Alive」表示端点在最近一次检查中返回了符合协议的响应。
- 它不代表某个 infohash 一定有节点，也不代表节点持有完整资源。
- Tracker 再多也无法补出所有节点都缺失的数据块。
- `aggressive` 和全量并行层会把 infohash 暴露给更多 Tracker 运营者，并产生更多网络请求。
- 带个人 passkey 的私有 Tracker 属于账户凭证，无法安全公开，因此不会收录。
- 当前离线项继续留在候选目录中，避免地区性或间歇性 Tracker 被永久丢失。

## 本地更新

项目只使用 Python 标准库：

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests
```

欢迎通过 Pull Request 补充公开来源，规则见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

## 许可与来源

[`sources.json`](sources.json) 记录每个来源地址和来源许可，生成记录保留来源归属。项目代码采用 GPL-3.0-or-later。
