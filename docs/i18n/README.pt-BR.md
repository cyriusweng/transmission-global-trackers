# Trackers globais para Transmission

[English](../../README.md)

Este projeto reúne trackers públicos de BitTorrent de várias fontes, remove duplicatas, verifica cada endereço diariamente e gera arranjos otimizados para o Transmission 4.1+.

- [`balanced`](../../lists/transmission/balanced.txt): perfil recomendado para o dia a dia, com poucos níveis paralelos e trackers de reserva.
- [`aggressive`](../../lists/transmission/aggressive.txt): uso temporário para swarms raros ou fracos.
- [`all`](../../lists/transmission/all.txt): todos os trackers UDP, HTTP e HTTPS verificados no momento.
- [`candidates`](../../lists/candidates/all.txt): inventário completo, inclusive endpoints atualmente indisponíveis.

Para adicionar trackers a um magnet:

```bash
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
```

Trackers privados com passkeys pessoais são excluídos. “Alive” confirma apenas uma resposta válida na última verificação; não garante peers nem um seed completo para um torrent específico.
