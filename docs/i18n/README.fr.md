# Trackers mondiaux pour Transmission

[English](../../README.md) · [简体中文](../../README.zh-CN.md)

Ce projet agrège des trackers BitTorrent publics provenant de plusieurs sources, conserve leur attribution, les vérifie chaque jour et produit des listes pratiques pour Transmission 4.1+, les autres clients BitTorrent, WebTorrent et les réseaux spécialisés.

## Choisir la bonne liste

| Liste | Utilisation |
| --- | --- |
| [`macos.txt`](../../lists/transmission/macos.txt) | Interface macOS de Transmission ; 12 trackers principaux sélectionnés. |
| [`magnet.txt`](../../lists/transmission/magnet.txt) | Ajout à un lien Magnet sans créer une URI démesurée. |
| [`balanced.txt`](../../lists/transmission/balanced.txt) | Réglage `default_trackers` par daemon ou RPC ; 12 niveaux parallèles, chacun avec deux secours. |
| [`aggressive.txt`](../../lists/transmission/aggressive.txt) | Temporairement pour un essaim rare ou faible ; jusqu’à 60 hôtes. |
| [`all.txt`](../../lists/transmission/all.txt) | Tous les trackers UDP, HTTP et HTTPS actuellement vérifiés. |
| [`candidates/all.txt`](../../lists/candidates/all.txt) | Inventaire complet, y compris les points hors ligne ; ne pas importer comme liste quotidienne. |
| [`webtorrent/all.txt`](../../lists/webtorrent/all.txt) | Trackers WS/WSS pour WebTorrent ; Transmission ne les prend pas en charge. |
| [`special/`](../../lists/special/) | I2P/Yggdrasil, uniquement si le réseau correspondant est configuré. |

## Transmission sur macOS : ajouter des trackers

1. Ouvrez [`macos.txt`](../../lists/transmission/macos.txt) et copiez ses 12 lignes.
2. Sélectionnez un seul transfert dans Transmission.
3. Ouvrez **View → Show Inspector**, puis l’onglet **Trackers**.
4. Cliquez sur **+**, collez les lignes dans le nouveau champ et validez.
5. Chaque ligne devient un niveau indépendant. Attendez quelques minutes pour les annonces et la découverte des pairs.

Utilisez `macos.txt` pour cette méthode. Coller `balanced.txt` dans l’interface macOS aplatit ses niveaux de secours. Les torrents privés interdisent souvent DHT, PeX et les trackers externes ; respectez toujours les règles du site.

## Enrichir un lien Magnet

```bash
git clone https://github.com/cyriusweng/transmission-global-trackers.git
cd transmission-global-trackers
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
python3 scripts/boost_magnet.py --profile balanced --open 'magnet:?xt=urn:btih:...'
```

La commande affiche un nouveau Magnet. `balanced` ajoute 12 trackers, `aggressive` jusqu’à 60, et `all` tous les trackers vérifiés pour le diagnostic. Les paramètres `tr=` existants sont conservés et dédupliqués.

## Trackers par défaut persistants

`default_trackers` suit BEP 12 : une nouvelle ligne indique un secours dans le même niveau ; une ligne vide crée un niveau parallèle. Utilisez [`balanced.txt`](../../lists/transmission/balanced.txt) avec un daemon ou un contrôleur RPC. L’interface macOS native ne propose pas de champ global persistant ; utilisez `macos.txt` par transfert ou enrichissez le Magnet.

## Autres clients

qBittorrent, Deluge et BiglyBT peuvent commencer avec [`best.txt`](../../lists/transmission/best.txt) ou [`all.txt`](../../lists/transmission/all.txt). aria2 et Motrix peuvent utiliser `all.txt` ou le convertir au format séparé par des virgules. WebTorrent doit utiliser `webtorrent/all.txt`.

## Mise à jour automatique

GitHub Actions exécute l’actualisation chaque jour à 03:17 UTC ; votre ordinateur peut rester éteint. Le runner agrège, effectue une vérification légère par protocole, met à jour l’historique, lance les tests et valide les modifications. Aucun contenu n’est téléchargé et le runner ne s’enregistre pas comme pair. Les résultats peuvent varier selon le pays, le FAI, le VPN ou IPv6.

## Limites et confidentialité

« Alive » confirme uniquement une réponse valide au dernier contrôle ; cela ne garantit ni pairs ni source complète pour un infohash. Aucun tracker ne recrée des données absentes de tout l’essaim. Les grands profils exposent l’infohash à davantage d’opérateurs. Les passkeys privées sont exclues car ce sont des identifiants de compte.

Reconstruction locale sans dépendance tierce :

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests
```
