# Trackers mondiaux pour Transmission

[English](../../README.md)

Ce projet agrège des trackers BitTorrent publics provenant de plusieurs sources, supprime les doublons, les vérifie chaque jour et produit des dispositions optimisées pour Transmission 4.1+.

- [`balanced`](../../lists/transmission/balanced.txt) : profil recommandé au quotidien, avec quelques niveaux parallèles et des trackers de secours.
- [`aggressive`](../../lists/transmission/aggressive.txt) : profil temporaire pour les essaims rares ou peu actifs.
- [`all`](../../lists/transmission/all.txt) : tous les trackers UDP, HTTP et HTTPS actuellement vérifiés.
- [`candidates`](../../lists/candidates/all.txt) : inventaire complet, y compris les points actuellement hors ligne.

Ajouter des trackers à un lien magnet :

```bash
python3 scripts/boost_magnet.py --profile balanced 'magnet:?xt=urn:btih:...'
```

Les trackers privés contenant une passkey personnelle sont exclus. « Alive » signifie seulement que le serveur a répondu correctement lors du dernier contrôle ; cela ne garantit ni pairs ni source complète pour un torrent donné.
