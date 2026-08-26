# Transmission용 글로벌 Tracker 모음

[English](../../README.md) · [简体中文](../../README.zh-CN.md)

여러 공개 출처에서 BitTorrent Tracker를 수집하고 중복을 제거한 뒤 매일 검증하여 Transmission 4.1+에 맞는 계층 구성을 생성합니다.

- [`balanced`](../../lists/transmission/balanced.txt): 일상 사용 권장. 적은 수의 병렬 Tier와 예비 Tracker를 함께 사용합니다.
- [`aggressive`](../../lists/transmission/aggressive.txt): 희귀하거나 약한 swarm에 일시적으로 사용합니다.
- [`all`](../../lists/transmission/all.txt): 현재 검증된 모든 UDP／HTTP／HTTPS Tracker입니다.
- [`candidates`](../../lists/candidates/all.txt): 현재 오프라인인 항목까지 포함한 전체 후보입니다.

Magnet 링크에 Tracker 추가:

```bash
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
```

개인 passkey가 포함된 비공개 Tracker는 제외합니다. “Alive”는 최근 검사에서 유효한 응답을 받았다는 뜻이며, 특정 Torrent의 peer나 완전한 seed를 보장하지 않습니다.
