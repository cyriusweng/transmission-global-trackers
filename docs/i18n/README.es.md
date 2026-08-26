# Trackers globales para Transmission

[English](../../README.md) · [简体中文](../../README.zh-CN.md)

El proyecto reúne trackers públicos de BitTorrent de múltiples fuentes, conserva su atribución, los valida a diario y genera listas prácticas para Transmission 4.1+, otros clientes BitTorrent, WebTorrent y redes especializadas.

## Elige la lista adecuada

| Lista | Cuándo usarla |
| --- | --- |
| [`macos.txt`](../../lists/transmission/macos.txt) | Interfaz de Transmission para macOS; 12 trackers principales seleccionados. |
| [`magnet.txt`](../../lists/transmission/magnet.txt) | Para añadir trackers a un Magnet URI sin crear un enlace enorme. |
| [`balanced.txt`](../../lists/transmission/balanced.txt) | Para `default_trackers` mediante daemon o RPC; 12 niveles paralelos con dos respaldos por nivel. |
| [`aggressive.txt`](../../lists/transmission/aggressive.txt) | Uso temporal para enjambres raros o débiles; hasta 60 hosts. |
| [`all.txt`](../../lists/transmission/all.txt) | Todos los trackers UDP, HTTP y HTTPS verificados actualmente. |
| [`candidates/all.txt`](../../lists/candidates/all.txt) | Inventario completo, incluidos endpoints hoy inaccesibles; no lo importes como lista diaria. |
| [`webtorrent/all.txt`](../../lists/webtorrent/all.txt) | Trackers WS/WSS para WebTorrent; Transmission no los admite. |
| [`special/`](../../lists/special/) | I2P/Yggdrasil; solo con la red correspondiente configurada. |

## Transmission en macOS: añadir trackers a una transferencia

1. Abre [`macos.txt`](../../lists/transmission/macos.txt) y copia sus 12 líneas.
2. Selecciona una sola transferencia en Transmission.
3. Abre **View → Show Inspector** y entra en la pestaña **Trackers**.
4. Pulsa **+**, pega las líneas en el nuevo campo y confirma.
5. Cada línea se añade como un nivel independiente. Espera unos minutos para los anuncios y el descubrimiento de pares.

Usa `macos.txt` en este flujo. Al pegar `balanced.txt`, la interfaz de macOS pierde la estructura de respaldos. Los torrents privados suelen prohibir DHT, PeX y trackers externos; no añadas trackers públicos salvo permiso expreso de las reglas del sitio.

## Mejorar un enlace Magnet

```bash
git clone https://github.com/cyriusweng/transmission-global-trackers.git
cd transmission-global-trackers
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
python3 scripts/boost_magnet.py --profile balanced --open 'magnet:?xt=urn:btih:...'
```

El comando imprime un Magnet nuevo. `balanced` añade 12 trackers; `aggressive`, hasta 60; `all`, todos los verificados y solo se recomienda para diagnóstico. Los parámetros `tr=` existentes se conservan y se eliminan duplicados.

## Trackers predeterminados persistentes

`default_trackers` sigue BEP 12: una línea nueva indica un respaldo en el mismo nivel y una línea en blanco crea un nivel paralelo. Usa [`balanced.txt`](../../lists/transmission/balanced.txt) con un daemon o controlador RPC. La interfaz nativa de macOS no expone un campo global persistente; usa `macos.txt` por transferencia o mejora primero el Magnet.

## Otros clientes

qBittorrent, Deluge y BiglyBT pueden empezar con [`best.txt`](../../lists/transmission/best.txt) o [`all.txt`](../../lists/transmission/all.txt). aria2 y Motrix pueden usar `all.txt` o convertirlo al formato separado por comas. WebTorrent debe usar `webtorrent/all.txt`.

## Actualización automática

GitHub Actions ejecuta la actualización todos los días a las 03:17 UTC; tu ordenador puede estar apagado. El runner agrega fuentes, hace una comprobación ligera por protocolo, actualiza el historial, ejecuta pruebas y confirma los cambios. No descarga contenido ni se registra como par. La conectividad de un runner de GitHub puede diferir según país, ISP, VPN o IPv6.

## Límites y privacidad

“Alive” solo confirma una respuesta válida en la última comprobación; no garantiza pares ni una semilla completa para un infohash. Ninguna lista reconstruye datos ausentes de todo el enjambre. Los perfiles grandes exponen el infohash a más operadores. Se excluyen trackers privados con passkeys personales porque son credenciales de cuenta.

Reconstrucción local, sin dependencias externas:

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests
```
