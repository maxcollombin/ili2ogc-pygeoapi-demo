# Fehlerbehebung und Grenzen

## Fehlerbehebung

| Symptom | Ursache und Abhilfe |
|---|---|
| `http://localhost:5000` antwortet nach `docker compose up` nicht | Der Loader ist nicht fertig: `pygeoapi` startet erst nach ihm. Die Logs verfolgen (`docker compose logs -f loader`). |
| Der Loader bricht mit einem Fehler ab | Ein Modell-Download ist fehlgeschlagen (Zugriff auf die INTERLIS-Modell-Repositories) oder eine Transferdatei besteht die Validierung nicht. Neu starten; die Meldung des fehlschlagenden `interlis`-Befehls lesen. |
| Port 5000 oder 5432 bereits belegt | Den betreffenden Dienst stoppen oder die Portzuordnung in `docker-compose.yml` ändern. |
| Leere Objektliste bei einer `bbox` in Metern | `bbox` wird als Grad gelesen. `bbox-crs=http://www.opengis.net/def/crs/EPSG/0/2056` hinzufügen. |
| Karte `/map` leer oder mit Fehler | Eine Karte ohne `bbox` ist leer. Ein Ausschnitt in EPSG:2056 ohne `bbox-crs` führt zu einem Fehler. Einen Ausschnitt im Bereich der Objekte angeben (Ausdehnung der Collection). |
| Kein Feld `place` in JSON-FG | `place` erscheint nur, wenn `crs` nicht CRS84 ist. |
| Die Karte der Punkte von `uebertragungsleitungen_punkte` existiert nicht | Diese Punkte werden ohne Karte bedient: Ihr offizielles Symbol wird nicht nachgebildet. |
| `/map` antwortet mit einem Fehler 500 | Gewisse ungültige Anfragen führen auf der Route `/map` von pygeoapi zu einem Fehler 500. Die Parameter prüfen. |
| Fehler 403 bei geodienste.ch (`/items`) | `crs=http://www.opengis.net/def/crs/EPSG/0/2056` hinzufügen. |
| `GetLegendGraphic` von geodienste.ch mit Fehler | `SLD_VERSION=1.1.0` hinzufügen. |
| Geladene Daten veraltet oder verändert | Der Loader erstellt die Schemas bei jedem Start neu: `docker compose down -v`, dann `docker compose up --build`. |

## Bekannte Grenzen

- **Eine Geometrie pro Collection.** pygeoapi lässt pro Collection nur einen Geometrietyp zu: Ein Datensatz mit mehreren Geometrien ergibt mehrere Collections.
- **Ergänzte Daten: Sachplan Militär.** Die publizierte Transferdatei enthält alle Objekte und Attribute, aber leere Geometrien. Diese stammen aus dem File-Geodatabase-Export desselben Datensatzes und werden über den Objektidentifikator zugeordnet; ergänzt wird nur die Geometrie. Dieser Mangel der publizierten Transferdatei ist dem Datenhalter zu melden.
- **Kartenviewer des Bundes.** map.geo.admin.ch importiert WMS- und WMTS-Dienste; seine Dokumentation erwähnt OGC API nicht. Die OGC-API-Maps-Collections der Demo lassen sich dort daher nicht direkt nutzen.
- **QGIS.** Die Dokumentation von QGIS 3.44 erwähnt OGC API - Features, aber nicht OGC API - Maps.
- **JSON-FG von pygeoapi.** Der Medientyp ist `application/geo+json`. `featureType` trägt den Namen der VIEW der Collection (im Dokument und je Objekt), wie in der Ausgabe von `convert-jsonfg` und in der Stilregel (`dataLayer.id`). Die Beschreibung der Collection (`/collections/{id}`) enthält ihn nicht: pygeoapi 0.24 hat keinen Konfigurationsschlüssel für `featureType`/`featureTypes`.
- **Proof of Concept.** ili2ogc hat den Status *Alpha*: nur INTERLIS 2, kein transaktionaler Dienst (die Demo aktualisiert nichts), keine INTERLIS-1-Modelle.
- **Über Referenzen gewonnene VIEW-Attribute.** Seit Version 0.9 von ili2ogc schreibt `convert-jsonfg` die VIEW-Attribute, die einer Referenz oder einer Struktur folgen. Eine Referenz auf einen Katalog, der nicht im Haupttransfer enthalten ist, kann nicht verfolgt werden: Der Katalog muss mit `--catalog DATEI.xtf` übergeben werden; ohne ihn fehlt der Wert, und ein Hinweis meldet es. Die Demo veröffentlicht aus der SQL-Datenbank, die die Kataloge mit den Daten lädt.
- **Geometrien und Darstellung.** 3D-Geometrien sind nur an synthetischen Beispielen geprüft; einige grafische Konzepte haben kein SLD-Äquivalent (durchgestrichener Text, Linienendsymbole, gewisse Schraffuren). Jeder nicht unterstützte Fall wird bei der Umwandlung gemeldet, nie stillschweigend ignoriert.
- **Koordinatensysteme.** Eine Domäne ohne Annotation `!!@CRS` ergibt eine weggelassene Geometrie; ein Dokument, das LV03 und LV95 mischt, wurde nicht ausprobiert.
- **Rendering-Engines.** MapServer liest das SLD mit seinen eigenen Standardwerten: Die Darstellung kann von der anderer Software (QGIS Server, ArcGIS Server) abweichen.
- **Stil des Bundes.** Die Massstabsbereiche der Sachpläne (geplante Massnahmen sichtbar ab 1:500 000) sind jene des gemeinsamen Darstellungsmodells; gewisse von den Produzenten gelieferte SLD widersprechen ihnen und werden nicht übernommen.

Die vollständigen Grenzen des Projekts stehen in der Dokumentation von ili2ogc.
