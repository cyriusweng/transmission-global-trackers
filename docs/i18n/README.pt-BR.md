# Trackers globais para Transmission

[English](../../README.md) · [简体中文](../../README.zh-CN.md)

O projeto reúne trackers públicos de BitTorrent de várias fontes, mantém a atribuição, verifica os endpoints diariamente e gera listas claras para Transmission 4.1+, outros clientes BitTorrent, WebTorrent e redes especializadas.

## Escolha a lista correta

| Lista | Quando usar |
| --- | --- |
| [`macos.txt`](../../lists/transmission/macos.txt) | Interface do Transmission no macOS; 12 trackers principais selecionados. |
| [`magnet.txt`](../../lists/transmission/magnet.txt) | Para acrescentar trackers a um Magnet sem deixar a URI enorme. |
| [`balanced.txt`](../../lists/transmission/balanced.txt) | `default_trackers` por daemon ou RPC; 12 tiers paralelos com dois backups em cada tier. |
| [`aggressive.txt`](../../lists/transmission/aggressive.txt) | Uso temporário para swarms raros ou fracos; até 60 hosts. |
| [`all.txt`](../../lists/transmission/all.txt) | Todos os trackers UDP, HTTP e HTTPS verificados no momento. |
| [`candidates/all.txt`](../../lists/candidates/all.txt) | Inventário completo, inclusive endpoints indisponíveis; não importe como lista diária. |
| [`webtorrent/all.txt`](../../lists/webtorrent/all.txt) | WS/WSS para WebTorrent; o Transmission não oferece suporte. |
| [`special/`](../../lists/special/) | I2P/Yggdrasil, apenas com a rede correspondente configurada. |

## Transmission no macOS: adicionar trackers

1. Abra [`macos.txt`](../../lists/transmission/macos.txt) e copie as 12 linhas.
2. Selecione somente uma transferência no Transmission.
3. Abra **View → Show Inspector** e a aba **Trackers**.
4. Clique em **+**, cole as linhas no novo campo e confirme.
5. Cada linha será adicionada como um tier independente. Aguarde alguns minutos para o announce e a descoberta de peers.

Use `macos.txt` nesse fluxo. Colar `balanced.txt` na interface do macOS elimina a estrutura de backups. Torrents privados normalmente proíbem DHT, PeX e trackers externos; respeite as regras do tracker privado.

## Reforçar um Magnet

```bash
git clone https://github.com/cyriusweng/transmission-global-trackers.git
cd transmission-global-trackers
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
python3 scripts/boost_magnet.py --profile balanced --open 'magnet:?xt=urn:btih:...'
```

O comando imprime um novo Magnet. `balanced` adiciona 12 trackers; `aggressive`, até 60; `all`, todos os verificados e deve ser usado só para diagnóstico. Parâmetros `tr=` existentes são preservados e duplicatas são removidas.

## Trackers padrão persistentes

`default_trackers` segue o BEP 12: uma quebra de linha indica backup no mesmo tier e uma linha vazia cria outro tier paralelo. Use [`balanced.txt`](../../lists/transmission/balanced.txt) com daemon ou RPC. A interface nativa do macOS não expõe um campo global persistente; use `macos.txt` por tarefa ou reforce o Magnet.

## Outros clientes

qBittorrent, Deluge e BiglyBT podem começar com [`best.txt`](../../lists/transmission/best.txt) ou [`all.txt`](../../lists/transmission/all.txt). aria2 e Motrix usam `all.txt` ou o formato separado por vírgulas exigido. WebTorrent usa `webtorrent/all.txt`.

## Atualização automática

O GitHub Actions atualiza diariamente às 03:17 UTC; seu computador pode ficar desligado. O runner agrega, faz uma verificação leve de protocolo, atualiza o histórico, executa testes e envia as mudanças. Nenhum conteúdo é baixado e o runner não se registra como peer. A conectividade pode variar conforme país, provedor, VPN ou IPv6.

## Limites e privacidade

“Alive” confirma apenas uma resposta válida na última verificação; não garante peers nem seed completo para um infohash. Trackers não recriam dados ausentes em todo o swarm. Perfis grandes expõem o infohash a mais operadores. Passkeys pessoais de trackers privados são credenciais e ficam excluídas.

Reconstrução local sem dependências externas:

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests
```
