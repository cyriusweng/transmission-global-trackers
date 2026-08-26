# Transmission용 글로벌 Tracker 모음

[English](../../README.md) · [简体中文](../../README.zh-CN.md)

여러 공개 출처에서 BitTorrent Tracker를 수집하고 출처 정보를 보존한 채 매일 검증합니다. Transmission 4.1+, 일반 BitTorrent 클라이언트, WebTorrent, 특수 네트워크용 목록을 따로 생성합니다.

## 알맞은 목록 선택

| 목록 | 용도 |
| --- | --- |
| [`macos.txt`](../../lists/transmission/macos.txt) | Transmission macOS GUI용 상위 12개 기본 Tracker. |
| [`magnet.txt`](../../lists/transmission/magnet.txt) | Magnet URI에 붙일 12개 Tracker. 링크가 지나치게 길어지는 것을 방지합니다. |
| [`balanced.txt`](../../lists/transmission/balanced.txt) | daemon/RPC의 `default_trackers`용. 12개 병렬 Tier와 Tier당 2개 예비 Tracker. |
| [`aggressive.txt`](../../lists/transmission/aggressive.txt) | 희귀하거나 약한 swarm에 임시 사용. 최대 60개 호스트. |
| [`all.txt`](../../lists/transmission/all.txt) | 현재 검증된 모든 UDP／HTTP／HTTPS Tracker. |
| [`candidates/all.txt`](../../lists/candidates/all.txt) | 현재 오프라인인 항목까지 포함한 전체 후보. 일상 목록으로 가져오지 마세요. |
| [`webtorrent/all.txt`](../../lists/webtorrent/all.txt) | WebTorrent용 WS／WSS. Transmission은 지원하지 않습니다. |
| [`special/`](../../lists/special/) | I2P／Yggdrasil 경로가 구성된 경우에만 사용합니다. |

## Transmission macOS: 기존 작업에 추가

1. [`macos.txt`](../../lists/transmission/macos.txt)를 열고 12줄을 모두 복사합니다.
2. Transmission에서 작업 하나만 선택합니다.
3. **View → Show Inspector**를 열고 **Trackers** 탭으로 이동합니다.
4. **+**를 누른 뒤 새 입력란에 여러 줄을 붙여 넣고 확인합니다.
5. 각 줄은 독립 Tier로 추가됩니다. announce와 peer discovery가 끝날 때까지 몇 분 기다립니다.

이 절차에는 `macos.txt`를 사용하세요. macOS GUI에 `balanced.txt`를 붙이면 예비 Tier 구조가 사라집니다. private torrent는 보통 DHT, PeX, 외부 Tracker를 금지하므로 사이트 규칙을 따르세요.

## Magnet 강화

```bash
git clone https://github.com/cyriusweng/transmission-global-trackers.git
cd transmission-global-trackers
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
python3 scripts/boost_magnet.py --profile balanced --open 'magnet:?xt=urn:btih:...'
```

새 Magnet이 출력됩니다. `balanced`는 12개, `aggressive`는 최대 60개, `all`은 검증된 전체를 추가하며 진단용으로만 권장합니다. 기존 `tr=` 값은 보존되고 중복은 제거됩니다.

## 영구 기본 Tracker

`default_trackers`는 BEP 12를 따릅니다. 한 번의 줄바꿈은 같은 Tier의 예비 Tracker이고, 빈 줄은 새 병렬 Tier입니다. daemon/RPC에서는 [`balanced.txt`](../../lists/transmission/balanced.txt)를 사용하세요. macOS 기본 GUI에는 영구 전역 입력란이 없으므로 작업마다 `macos.txt`를 적용하거나 Magnet을 먼저 강화합니다.

## 다른 클라이언트

qBittorrent, Deluge, BiglyBT는 [`best.txt`](../../lists/transmission/best.txt) 또는 [`all.txt`](../../lists/transmission/all.txt)를 사용할 수 있습니다. aria2/Motrix는 `all.txt` 또는 필요한 쉼표 형식을 사용합니다. WebTorrent는 `webtorrent/all.txt`를 사용합니다.

## 자동 업데이트

GitHub Actions가 매일 03:17 UTC에 실행되므로 개인 컴퓨터는 꺼져 있어도 됩니다. 클라우드 Runner가 집계, 가벼운 프로토콜 검사, 이력 갱신, 테스트와 커밋을 수행합니다. Torrent 본문을 받지 않고 peer로 등록하지 않습니다. 국가, ISP, VPN, IPv6에 따라 결과가 다를 수 있습니다.

## 제한과 개인정보

“Alive”는 최근 검사에서 유효 응답을 받았다는 뜻일 뿐 특정 infohash의 peer나 완전한 seed를 보장하지 않습니다. swarm 전체에 없는 데이터는 Tracker로 복구할 수 없습니다. 큰 프로필은 infohash를 더 많은 운영자에게 노출합니다. 개인 passkey는 계정 자격 증명이므로 제외합니다.

추가 패키지 없이 로컬 재생성:

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests
```
