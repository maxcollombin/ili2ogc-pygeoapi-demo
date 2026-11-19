# Notebooks : élaborer et publier un modèle dérivé

Exercices guidés, en français, sur la chaîne du dépôt : un modèle dérivé (VIEW), une représentation graphique (règle graphique et signatures), les commandes d'ili2ogc, la publication avec pygeoapi.

| Notebook | Contenu |
|---|---|
| `00_installation.ipynb` | installer `ili2ogc` 0.9.0 (`%pip install`), vérifier l'environnement, où vont les fichiers |
| `01_vue.ipynb` | écrire une VIEW `PROJECTION OF`, puis `JOIN OF ... WHERE` (cellules `%%writefile`) ; `build`, `convert-sql`, lecture du `CREATE VIEW` (modèle Planungszonen) |
| `02_representation.ipynb` | écrire une règle graphique `GRAPHIC` et ses signatures XTF ; `convert-sld`, lecture du SLD |
| `03_ili2ogc.ipynb` | la chaîne `fetch-models`, `validate-xtf`, `convert-jsonschema`, `convert-jsonfg`, `convert-sql`, `import-xtf` sur un transfert du dépôt |
| `04_publication.ipynb` | publier sans base de données avec pygeoapi (GeoJSON), interroger l'API, afficher la carte ; puis la pile Docker du dépôt (PostGIS), démarrée et arrêtée depuis le notebook |

À suivre dans l'ordre. Chaque notebook donne son objectif, des étapes numérotées, des cellules « À vous » avec une cellule de vérification (`assert`) et une solution repliée, à ouvrir après avoir essayé. Les notebooks sont livrés sans sorties.

Les commandes sont écrites telles qu'on les taperait dans un terminal : une cellule `!interlis convert-sql ...` appelle l'outil, une cellule `%%writefile` écrit un fichier (les modèles `.ili`). Les chemins sont relatifs à `notebooks/`, le dossier de travail de Jupyter : `../data` et `../collections` (dépôt), `modeles/` (modèles téléchargés), `sorties/` (tout ce que les notebooks produisent).

## Ce qui exige Internet

- `fetch-models` (notebooks 01 à 04) télécharge les modèles INTERLIS officiels depuis `models.interlis.ch`, `models.geo.admin.ch` et `models.kgk-cgc.ch`. Les autres commandes d'ili2ogc travaillent sur des fichiers locaux et n'ont pas besoin du réseau.
- L'installation des paquets Python (`pip`, `uv`).
- Le fond de carte OpenStreetMap du notebook 04 est chargé par le navigateur.

Les données (`data/`, `collections/`) viennent du dépôt. Seule la fin du notebook 04 utilise Docker (`docker compose`, port 5000 libre) ; les notebooks 00 à 03 n'ont besoin ni de Docker ni d'une base de données.

## Démarrer

### Sans rien installer : dans le navigateur

[![Ouvrir dans Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/geostandards-ch/ili2ogc-pygeoapi-demo/main?urlpath=lab/tree/notebooks/00_installation.ipynb)

Un clic ouvre JupyterLab avec les notebooks et tout ce qu'il faut. La première ouverture prépare l'environnement et peut prendre une dizaine de minutes ; les suivantes sont plus rapides. Les notebooks 00 à 03 y tournent ; la fin du notebook 04 (pile Docker) demande un ordinateur avec Docker. Binder efface le travail à la fermeture de la session : télécharger les fichiers à garder.

### Sur votre ordinateur

```bash
git clone https://github.com/geostandards-ch/ili2ogc-pygeoapi-demo.git
cd ili2ogc-pygeoapi-demo/notebooks
uv venv --seed && source .venv/bin/activate     # sous Windows : .venv\Scripts\activate
uv pip install -r requirements.txt jupyterlab
jupyter lab
```

Python 3.10 ou plus récent.

## Fichiers

- `modeles/`, `sorties/` : modèles téléchargés et sorties des notebooks, créés à l'exécution ; ignorés par git.
