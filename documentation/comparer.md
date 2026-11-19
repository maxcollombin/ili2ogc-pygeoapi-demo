# Comparer avec d'autres services

La comparaison porte sur un même thème publié par la démo et par un autre service : ce que le service expose (attributs, noms de champs), comment (géométrie, système de coordonnées, formats, versions) et avec quel dessin (symbologie).

## Thèmes comparés

| Thème | Démo | Service de comparaison |
|---|---|---|
| Distances par rapport à la forêt (Glaris) | `waldabstandslinien` | geodienste.ch, thème `npl_waldabstandslinien` (WMS, WFS, OGC API - Features) |
| Plans directeurs, énergies renouvelables (Schaffhouse) | `richtplanung`, `richtplanung_punkte` | geodienste.ch, thème `richtplanung_erneuerbare_energien` |
| Lignes de transport d'électricité | `uebertragungsleitungen_*` | WMS de la Confédération, couche `ch.bfe.sachplan-uebertragungsleitungen_kraft` |

Les adresses et la connexion à chaque service sont décrites dans [QGIS pas à pas](qgis.md).

## Tableau : Waldabstandslinien

| Critère | Démo | geodienste.ch |
|---|---|---|
| Attributs de la ligne | `publiziertab`, `publiziertbis`, `rechtsstatus`, `bemerkungen` | `publiziert_ab`, `publiziert_bis`, `rechtsstatus`, `bemerkungen` |
| Type de la distance | `typ_code`, `typ_bezeichnung`, `typ_abkuerzung`, `typ_verbindlichkeit` | `code`, `bezeichnung`, `abkuerzung`, `verbindlichkeit` |
| Attributs propres au service | `t_ili_tid` (identifiant INTERLIS) | `kanton`, `dokument` (documents liés, en JSON) |
| Identifiant d'objet | identifiant du transfert (`186`) | numéro interne (`2225374`) |
| Valeur absente | `null` | chaîne vide |
| Dates | type `date` dans le schéma | chaîne |
| Étendue | un canton | plusieurs cantons, à filtrer sur `kanton` |
| Géométrie | ligne | ligne |
| Système de coordonnées | stockage EPSG:2056 ; GeoJSON en CRS84 par défaut, EPSG:2056 avec `crs` | EPSG:2056 ; l'OGC API exige `crs=...2056` |
| Formats d'objets | GeoJSON, JSON-FG, HTML, CSV, JSON-LD | WFS : GML 3.2, 3.1.1, 2.1.2, GeoJSON ; OGC API : GeoJSON, HTML |
| Cartes | OGC API - Maps (PNG) et style SLD INTERLIS | WMS 1.3.0 (EPSG:2056, 3857, 4326) |
| Queryables et schéma | oui (`/queryables`, `/schema`) | non pour l'OGC API (réponse 404) ; `DescribeFeatureType` pour le WFS |
| Versions | OGC API - Features partie 1, 2 (CRS) et 3 (queryables), OGC API - Maps | OGC API - Features partie 1 et 2 ; WFS 1.0.0, 1.1.0 et 2.0.0 ; WMS 1.3.0 |
| Accès | local, sans clé | public, sans clé ; conditions d'utilisation, frais possibles selon le canton |

## Tableau : plan directeur, énergies renouvelables

| Critère | Démo | geodienste.ch |
|---|---|---|
| Découpage des collections | une collection par géométrie (`richtplanung`, `richtplanung_punkte`), la forme d'énergie est l'attribut `energieform` | un type d'objet par forme d'énergie et par géométrie (`windenergie_flaechen`, ...), plus des types de métadonnées |
| Noms de champs | `beschrieb`, `beschlussdatumkanton` | `beschreibung`, `beschlussdatum_kanton` |
| Champs communs | `objektbezeichnung`, `objektart`, `energieform`, `genehmigungsdatum`, `weblink`, `bemerkungen`, `kanton` | idem |
| Étendue | canton de Schaffhouse | plusieurs cantons |

## Tableau : lignes de transport d'électricité

Le leitungszug n° 203 Innertkirchen-Ulrichen figure des deux côtés (mesure `pm146`, corridor de projet, dans le WMS ; mesure `pm148`, suppression d'une ligne existante, dans `uebertragungsleitungen_linien`). Les deux services reprennent les identifiants du plan sectoriel (`pm...`).

| Critère | Démo (`uebertragungsleitungen`) | WMS de la Confédération |
|---|---|---|
| Identifiant | `t_ili_tid` | `stabil_id` |
| Nom | `name_de`, `name_fr`, `name_it` (+ `name_en`, `name_rm`) | `plname_de`, `plname_fr`, `plname_it` |
| Type de mesure | `type_name_de`, ... | `meastype_text_de`, ... |
| Niveau de coordination | `coord_name_de`, ... | `coordlevel_text_de`, ... |
| Statut | `status_name_de`, ... | `plstatus_text_de`, ... |
| Date de validité | `modinfo_validfrom` (date et heure ISO) | `validfrom` (`22.02.2023`) |
| Autres attributs | références résolues vers l'installation (`facility_*`), `description_*` | |
| Accès aux attributs | OGC API - Features | `GetFeatureInfo` en `text/plain`, `text/xml` ou `application/vnd.ogc.gml` |
| Cartes | OGC API - Maps | WMS 1.3.0 |

## Procédure

1. Dans QGIS, charger la couche de la démo, puis la couche du service de comparaison ([QGIS pas à pas](qgis.md)), sur le fond swisstopo.
2. Zoomer sur une zone où les deux couches ont des objets (Glaris pour les Waldabstandslinien, Schaffhouse pour la Richtplanung). Alterner la visibilité des couches : les objets coïncident-ils ?
3. Ouvrir la table attributaire des deux couches. Noter les champs présents d'un seul côté, les noms qui diffèrent, les valeurs absentes (`null` ou chaîne vide) et les types.
4. Utiliser **Identifier** sur un même objet dans les deux couches et rapprocher valeur par valeur.
5. Ouvrir les propriétés de chaque couche (onglet **Information**) : système de coordonnées, type de géométrie, étendue, nombre d'objets.
6. Comparer la symbologie : onglet **Symbologie** des couches vectorielles de la démo (QGIS applique son propre style aux objets reçus en OGC API - Features), puis les couches WMS, qui arrivent déjà dessinées. Pour voir le style INTERLIS de la démo, utiliser sa carte `/map` dans un navigateur ([Explorer](explorer.md)).
7. Comparer la légende : pour le WMS de geodienste.ch, [`GetLegendGraphic`](https://geodienste.ch/db/npl_waldabstandslinien/deu?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetLegendGraphic&LAYER=waldabstandslinien&FORMAT=image/png&SLD_VERSION=1.1.0) exige le paramètre `SLD_VERSION`.

Requêtes équivalentes en ligne de commande, pour la comparaison d'attributs :

```bash
# Démo
curl 'http://localhost:5000/collections/waldabstandslinien/items?f=json&limit=1'

# geodienste.ch, OGC API - Features
curl 'https://geodienste.ch/db/npl_waldabstandslinien/deu/ogcapi/collections/waldabstandslinien/items?f=json&limit=1&crs=http://www.opengis.net/def/crs/EPSG/0/2056'

# geodienste.ch, WFS 2.0.0, GeoJSON
curl 'https://geodienste.ch/db/npl_waldabstandslinien/deu?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAMES=ms:waldabstandslinien&COUNT=1&OUTPUTFORMAT=application/json;%20subtype=geojson'

# Confédération, WMS, attributs au point (LV95, text/plain)
curl 'https://wms.geo.admin.ch/?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetFeatureInfo&LAYERS=ch.bfe.sachplan-uebertragungsleitungen_kraft&QUERY_LAYERS=ch.bfe.sachplan-uebertragungsleitungen_kraft&CRS=EPSG:2056&BBOX=2665687,1148644,2669687,1152644&WIDTH=400&HEIGHT=400&I=200&J=200&INFO_FORMAT=text/plain&FEATURE_COUNT=5'
```

## Ce que la comparaison montre

- **Mêmes objets, mêmes valeurs.** Sur les exemples examinés (Waldabstandslinien, plan sectoriel), les valeurs d'attributs coïncident (statut, type, dates, noms), seuls les noms de champs et la présentation changent.
- **Les noms de champs sont une décision de service, non une donnée.** Chaque service nomme ses champs à sa façon (`publiziertab` ou `publiziert_ab`, `beschrieb` ou `beschreibung`, `plname_de` ou `name_de`). Dans la démo, ils viennent des VIEW INTERLIS : modifier une VIEW change le service, sans autre code. Un client qui passe d'un service à l'autre doit refaire sa correspondance de champs.
- **Le découpage en collections diffère aussi.** geodienste.ch sépare les formes d'énergie en types d'objets distincts ; la démo les regroupe et les distingue par un attribut.
- **L'étendue n'est pas la même.** geodienste.ch agrège plusieurs cantons dans un service ; la démo publie un seul jeu cantonal à la fois.
- **Le système de coordonnées est géré différemment.** geodienste.ch travaille en EPSG:2056 et impose `crs` sur l'OGC API ; la démo stocke en EPSG:2056, répond en CRS84 par défaut et accepte `crs` et `bbox-crs`.
- **La démo ajoute des fonctions que les services comparés n'ont pas** : JSON-FG, queryables et schéma, cartes OGC API - Maps. Inversement, les services publics offrent le WMS, le WFS et la couverture de nombreux cantons.
- **La symbologie suit des chemins différents.** Les couches WMS arrivent dessinées par leur éditeur ; dans la démo, le style est issu de la symbologie décrite en INTERLIS, et l'objet reçu en OGC API - Features n'en porte aucun.
