# Trackers globales para Transmission

[English](../../README.md)

Este proyecto agrega trackers públicos de BitTorrent desde múltiples fuentes, elimina duplicados, los valida cada día y genera diseños optimizados para Transmission 4.1+.

- [`balanced`](../../lists/transmission/balanced.txt): opción recomendada para uso diario; pocos niveles paralelos con trackers de respaldo.
- [`aggressive`](../../lists/transmission/aggressive.txt): uso temporal para enjambres raros o débiles.
- [`all`](../../lists/transmission/all.txt): todos los trackers UDP, HTTP y HTTPS verificados actualmente.
- [`candidates`](../../lists/candidates/all.txt): inventario completo, incluidos los puntos hoy inaccesibles.

Para añadir trackers a un enlace magnet:

```bash
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
```

Se excluyen los trackers privados con passkeys personales. «Alive» solo confirma una respuesta válida en la última comprobación; no garantiza pares ni una semilla completa para un torrent concreto.
