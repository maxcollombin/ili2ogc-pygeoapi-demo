# Dépannage et limites

## Dépannage

| Symptôme | Cause et remède |
|---|---|
| `http://localhost:5000` ne répond pas après `docker compose up` | Le chargeur n'a pas terminé : `pygeoapi` démarre seulement après lui. Suivre les journaux (`docker compose logs -f loader`). |
| Le chargeur s'arrête en erreur | Un téléchargement de modèle a échoué (accès aux dépôts de modèles INTERLIS) ou un transfert ne passe pas la validation. Relancer ; lire le message de la commande `interlis` qui échoue. |
| Port 5000 ou 5432 déjà utilisé | Arrêter le service concerné, ou modifier la correspondance de ports dans `docker-compose.yml`. |
| Liste d'objets vide avec un `bbox` en mètres | `bbox` est lu en degrés. Ajouter `bbox-crs=http://www.opengis.net/def/crs/EPSG/0/2056`. |
| Carte `/map` vide ou en erreur | Une carte sans `bbox` est vide. Une emprise en EPSG:2056 sans `bbox-crs` donne une erreur. Donner une emprise de la zone des objets (étendue de la collection). |
| Pas de champ `place` en JSON-FG | `place` n'apparaît que si `crs` n'est pas CRS84. |
| La carte des points de `uebertragungsleitungen_punkte` n'existe pas | Ces points sont servis sans carte : leur symbole officiel n'est pas reproduit. |
| `/map` répond par une erreur 500 | Certaines requêtes invalides provoquent une erreur 500 sur la route `/map` de pygeoapi. Vérifier les paramètres. |
| Erreur 403 sur geodienste.ch (`/items`) | Ajouter `crs=http://www.opengis.net/def/crs/EPSG/0/2056`. |
| `GetLegendGraphic` geodienste.ch en erreur | Ajouter `SLD_VERSION=1.1.0`. |
| Données chargées anciennes ou modifiées | Le chargeur recrée les schémas à chaque démarrage : `docker compose down -v` puis `docker compose up --build`. |

## Limites connues

- **Une géométrie par collection.** pygeoapi n'admet qu'un type de géométrie par collection : un jeu de données à plusieurs géométries donne plusieurs collections.
- **Donnée complétée : plan sectoriel militaire.** Le transfert publié contient tous les objets et attributs, mais des géométries vides. Elles proviennent de l'export File Geodatabase du même jeu, appariées par identifiant d'objet ; seule la géométrie est ajoutée. Ce défaut du transfert publié est à signaler à son détenteur.
- **Visionneuse de la Confédération.** map.geo.admin.ch importe des services WMS et WMTS ; sa documentation ne mentionne pas OGC API. Les collections OGC API - Maps de la démo ne s'y consomment donc pas directement.
- **QGIS.** La documentation de QGIS 3.44 mentionne OGC API - Features mais pas OGC API - Maps.
- **JSON-FG de pygeoapi.** Le type de média est `application/geo+json`. `featureType` porte le nom de la VIEW de la collection (par document et par objet), comme dans la sortie de `convert-jsonfg` et dans la règle de style (`dataLayer.id`). La description de la collection (`/collections/{id}`) ne porte pas `featureTypes`, propriété facultative de la Part 2 d'OGC API – Common : pygeoapi 0.24 n'a pas de clé de configuration pour la publier.
- **Proof of Concept.** ili2ogc est au statut *alpha* : INTERLIS 2 uniquement, pas de service transactionnel (la démo ne met rien à jour), pas de modèles INTERLIS 1.
- **Attributs de VIEW obtenus par référence.** Depuis la version 0.9 d'ili2ogc, `convert-jsonfg` écrit les attributs de VIEW qui suivent une référence ou une structure. Une référence vers un catalogue absent du transfert principal ne peut pas être suivie : il faut passer le catalogue avec `--catalog FICHIER.xtf` ; sans lui, la valeur est omise et une note le signale. La démo publie depuis la base SQL, qui charge les catalogues avec les données.
- **Géométries et représentation.** Les géométries 3D ne sont vérifiées que sur des exemples synthétiques ; quelques notions graphiques n'ont pas d'équivalent SLD (texte barré, symboles de fin de ligne, certaines hachures). Chaque cas non pris en charge est signalé à la conversion, jamais ignoré en silence.
- **Systèmes de coordonnées.** Un domaine sans annotation `!!@CRS` donne une géométrie omise ; un document mêlant LV03 et LV95 n'a pas été essayé.
- **Moteurs de rendu.** MapServer lit le SLD avec ses propres défauts : le rendu peut différer de celui d'autres logiciels (QGIS Server, ArcGIS Server).
- **Style de la Confédération.** Les plages d'échelle des plans sectoriels (mesures planifiées visibles à partir du 1:500 000) sont celles du modèle de présentation commun ; certains SLD fournis par les producteurs les contredisent et ne sont pas repris.

Les limites complètes du projet figurent dans la documentation d'ili2ogc.
