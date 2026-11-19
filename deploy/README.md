# Publier et maintenir le démonstrateur

Pas à pas pour la personne qui maintient le dépôt. Le contexte (pourquoi ces choix, ce qui a été essayé, ce qui reste à décider)
est dans l'annexe « Reprise du démonstrateur » du rapport du projet.

## 1. Lancer la pile en local

Prérequis : Docker avec Docker Compose, accès à Internet.

```bash
docker compose up --build        # l'API répond sur http://localhost:5000 une fois le chargement terminé
docker compose down              # arrêt ; -v supprime aussi le volume des styles
```

Le chargeur télécharge les modèles, valide les transferts, crée les schémas, importe les objets et écrit les styles SLD, puis
s'arrête ; pygeoapi démarre ensuite. Comptez quelques minutes la première fois.

## 2. Publier le site de documentation (GitHub Pages)

Le site est français et allemand (`mkdocs-static-i18n`). Au choix :

**a. Branche `gh-pages`**, sans fichier de workflow :

```bash
pip install -r requirements-docs.txt
mkdocs gh-deploy --force
```

Puis Settings, Pages : source « Deploy from a branch », branche `gh-pages`, dossier racine.

**b. GitHub Actions** : copier `deploy/pages.yml` dans `.github/workflows/pages.yml` (réservé aux personnes qui administrent le
dépôt), puis Settings, Pages : source « GitHub Actions ». Le site se reconstruit à chaque modification de `documentation/`, de
`mkdocs.yml` ou de `requirements-docs.txt`.

Tester avant de publier : `mkdocs build --strict -d /tmp/site`.

## 3. Rafraîchir les exemples de réponses de l'API

Pile lancée et chargement terminé :

```bash
python scripts/snapshot.py          # écrit documentation/snapshot/
```

Puis republier le site (étape 2).

## 4. Notebooks sur Binder (notebooks 00 à 03)

Aucune action : `binder/environment.yml` suffit (Python 3.12 et les dépendances). Lien à placer dans le README ou sur le site :

```
https://mybinder.org/v2/gh/<compte>/<dépôt>/<branche>?urlpath=lab/tree/notebooks/00_installation.ipynb
```

La première ouverture construit l'image (une dizaine de minutes lors de l'essai) ; les suivantes utilisent le cache. Pour amorcer la
construction à l'avance : ouvrir le lien une fois. Le notebook 04 a besoin de Docker : il ne tourne pas sur Binder.

## 5. Pile complète sur GitHub Codespaces

Code, Codespaces, « Create codespace on main ». `.devcontainer/devcontainer.json` lance `docker compose up --build -d` et transmet le
port 5000. Chaque personne consomme son propre quota gratuit ; un codespace s'arrête seul après 30 minutes d'inactivité.

## 6. À la publication d'une nouvelle version d'ili2ogc

Mettre la même version dans `loader/Dockerfile`, `notebooks/requirements.txt`, `binder/environment.yml` et la cellule d'installation du notebook 00, relancer la pile, exécuter `notebooks/run_all.sh`, vérifier
que le chargeur se termine sans erreur, puis rafraîchir les exemples de réponses (étape 3) et republier le site (étape 2).

## 7. Sécurité

Le port de la base n'est publié que sur `127.0.0.1` ; pygeoapi se connecte avec le rôle `reader` (lecture seule) créé par le chargeur ;
aucun mot de passe de production n'est dans le dépôt (ceux de la démo sont jetables). Ne pas publier le port de la base sur le réseau.

## 8. Contrôler les notebooks de bout en bout

```bash
cd notebooks && ./run_all.sh [dossier-de-sortie]
```

Le script crée un environnement neuf (`uv`), exécute les notebooks avec `jupyter nbconvert --execute`, une première fois avec les
solutions pour vérifier qu'ils passent, une seconde sans pour vérifier que chaque exercice échoue à sa cellule de vérification. Il
demande Docker pour la fin du notebook 04 (le port 5000 doit être libre ; le notebook arrête la pile). Les fichiers `run_all.sh` et
`_controle.py` ne servent qu'à cela.
