# Vergleich mit anderen Diensten

Der Vergleich betrifft dasselbe Thema, das von der Demo und von einem anderen Dienst veröffentlicht wird: was der Dienst anbietet (Attribute, Feldnamen), wie (Geometrie, Koordinatensystem, Formate, Versionen) und mit welcher Zeichnung (Darstellung).

## Verglichene Themen

| Thema | Demo | Vergleichsdienst |
|---|---|---|
| Waldabstandslinien (Glarus) | `waldabstandslinien` | geodienste.ch, Thema `npl_waldabstandslinien` (WMS, WFS, OGC API - Features) |
| Richtplanung erneuerbare Energien (Schaffhausen) | `richtplanung`, `richtplanung_punkte` | geodienste.ch, Thema `richtplanung_erneuerbare_energien` |
| Übertragungsleitungen | `uebertragungsleitungen_*` | WMS des Bundes, Layer `ch.bfe.sachplan-uebertragungsleitungen_kraft` |

Die Adressen und die Verbindung zu jedem Dienst sind in [QGIS Schritt für Schritt](qgis.md) beschrieben.

## Tabelle: Waldabstandslinien

| Kriterium | Demo | geodienste.ch |
|---|---|---|
| Attribute der Linie | `publiziertab`, `publiziertbis`, `rechtsstatus`, `bemerkungen` | `publiziert_ab`, `publiziert_bis`, `rechtsstatus`, `bemerkungen` |
| Typ des Abstands | `typ_code`, `typ_bezeichnung`, `typ_abkuerzung`, `typ_verbindlichkeit` | `code`, `bezeichnung`, `abkuerzung`, `verbindlichkeit` |
| Dienstspezifische Attribute | `t_ili_tid` (INTERLIS-Identifikator) | `kanton`, `dokument` (verknüpfte Dokumente, als JSON) |
| Objektidentifikator | Identifikator der Transferdatei (`186`) | interne Nummer (`2225374`) |
| Fehlender Wert | `null` | leere Zeichenkette |
| Daten | Typ `date` im Schema | Zeichenkette |
| Ausdehnung | ein Kanton | mehrere Kantone, nach `kanton` zu filtern |
| Geometrie | Linie | Linie |
| Koordinatensystem | Speicherung EPSG:2056; GeoJSON standardmässig in CRS84, EPSG:2056 mit `crs` | EPSG:2056; die OGC API verlangt `crs=...2056` |
| Formate der Objekte | GeoJSON, JSON-FG, HTML, CSV, JSON-LD | WFS: GML 3.2, 3.1.1, 2.1.2, GeoJSON; OGC API: GeoJSON, HTML |
| Karten | OGC API - Maps (PNG) und INTERLIS-SLD-Stil | WMS 1.3.0 (EPSG:2056, 3857, 4326) |
| Queryables und Schema | ja (`/queryables`, `/schema`) | nicht bei der OGC API (Antwort 404); `DescribeFeatureType` beim WFS |
| Versionen | OGC API - Features Teil 1, 2 (CRS) und 3 (Queryables), OGC API - Maps | OGC API - Features Teil 1 und 2; WFS 1.0.0, 1.1.0 und 2.0.0; WMS 1.3.0 |
| Zugang | lokal, ohne Schlüssel | öffentlich, ohne Schlüssel; Nutzungsbedingungen, je nach Kanton mögliche Gebühren |

## Tabelle: Richtplanung erneuerbare Energien

| Kriterium | Demo | geodienste.ch |
|---|---|---|
| Aufteilung in Collections | eine Collection pro Geometrie (`richtplanung`, `richtplanung_punkte`), die Energieform ist das Attribut `energieform` | eine Objektart pro Energieform und Geometrie (`windenergie_flaechen`, ...), dazu Metadaten-Objektarten |
| Feldnamen | `beschrieb`, `beschlussdatumkanton` | `beschreibung`, `beschlussdatum_kanton` |
| Gemeinsame Felder | `objektbezeichnung`, `objektart`, `energieform`, `genehmigungsdatum`, `weblink`, `bemerkungen`, `kanton` | identisch |
| Ausdehnung | Kanton Schaffhausen | mehrere Kantone |

## Tabelle: Übertragungsleitungen

Der Leitungszug Nr. 203 Innertkirchen-Ulrichen kommt auf beiden Seiten vor (Massnahme `pm146`, Projektkorridor, im WMS; Massnahme `pm148`, Aufhebung einer bestehenden Leitung, in `uebertragungsleitungen_linien`). Beide Dienste übernehmen die Identifikatoren des Sachplans (`pm...`).

| Kriterium | Demo (`uebertragungsleitungen`) | WMS des Bundes |
|---|---|---|
| Identifikator | `t_ili_tid` | `stabil_id` |
| Name | `name_de`, `name_fr`, `name_it` (+ `name_en`, `name_rm`) | `plname_de`, `plname_fr`, `plname_it` |
| Massnahmentyp | `type_name_de`, ... | `meastype_text_de`, ... |
| Koordinationsstand | `coord_name_de`, ... | `coordlevel_text_de`, ... |
| Status | `status_name_de`, ... | `plstatus_text_de`, ... |
| Gültigkeitsdatum | `modinfo_validfrom` (ISO-Datum mit Uhrzeit) | `validfrom` (`22.02.2023`) |
| Weitere Attribute | aufgelöste Referenzen auf die Anlage (`facility_*`), `description_*` | |
| Zugang zu den Attributen | OGC API - Features | `GetFeatureInfo` als `text/plain`, `text/xml` oder `application/vnd.ogc.gml` |
| Karten | OGC API - Maps | WMS 1.3.0 |

## Vorgehen

1. In QGIS den Layer der Demo laden, dann den Layer des Vergleichsdienstes ([QGIS Schritt für Schritt](qgis.md)), über der Hintergrundkarte von swisstopo.
2. In einen Bereich zoomen, in dem beide Layer Objekte haben (Glarus für die Waldabstandslinien, Schaffhausen für die Richtplanung). Die Sichtbarkeit der Layer abwechselnd ein- und ausschalten: Fallen die Objekte zusammen?
3. Die Attributtabelle beider Layer öffnen. Felder festhalten, die nur auf einer Seite vorkommen, abweichende Namen, fehlende Werte (`null` oder leere Zeichenkette) und die Typen.
4. Mit **Objekte abfragen** dasselbe Objekt in beiden Layern identifizieren und Wert für Wert vergleichen.
5. Die Eigenschaften jedes Layers öffnen (Reiter **Information**): Koordinatensystem, Geometrietyp, Ausdehnung, Anzahl Objekte.
6. Die Darstellung vergleichen: Reiter **Symbolisierung** der Vektorlayer der Demo (QGIS wendet auf die über OGC API - Features empfangenen Objekte seinen eigenen Stil an), dann die WMS-Layer, die bereits gezeichnet ankommen. Um den INTERLIS-Stil der Demo zu sehen, ihre Karte `/map` im Browser verwenden ([Erkunden](explorer.md)).
7. Die Legende vergleichen: Beim WMS von geodienste.ch verlangt [`GetLegendGraphic`](https://geodienste.ch/db/npl_waldabstandslinien/deu?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetLegendGraphic&LAYER=waldabstandslinien&FORMAT=image/png&SLD_VERSION=1.1.0) den Parameter `SLD_VERSION`.

Gleichwertige Abfragen auf der Kommandozeile, für den Attributvergleich:

```bash
# Demo
curl 'http://localhost:5000/collections/waldabstandslinien/items?f=json&limit=1'

# geodienste.ch, OGC API - Features
curl 'https://geodienste.ch/db/npl_waldabstandslinien/deu/ogcapi/collections/waldabstandslinien/items?f=json&limit=1&crs=http://www.opengis.net/def/crs/EPSG/0/2056'

# geodienste.ch, WFS 2.0.0, GeoJSON
curl 'https://geodienste.ch/db/npl_waldabstandslinien/deu?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAMES=ms:waldabstandslinien&COUNT=1&OUTPUTFORMAT=application/json;%20subtype=geojson'

# Bund, WMS, Attribute am Punkt (LV95, text/plain)
curl 'https://wms.geo.admin.ch/?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetFeatureInfo&LAYERS=ch.bfe.sachplan-uebertragungsleitungen_kraft&QUERY_LAYERS=ch.bfe.sachplan-uebertragungsleitungen_kraft&CRS=EPSG:2056&BBOX=2665687,1148644,2669687,1152644&WIDTH=400&HEIGHT=400&I=200&J=200&INFO_FORMAT=text/plain&FEATURE_COUNT=5'
```

## Was der Vergleich zeigt

- **Dieselben Objekte, dieselben Werte.** Bei den untersuchten Beispielen (Waldabstandslinien, Sachplan) stimmen die Attributwerte überein (Status, Typ, Daten, Namen); nur die Feldnamen und die Darstellung ändern sich.
- **Die Feldnamen sind eine Entscheidung des Dienstes, keine Datengrösse.** Jeder Dienst benennt seine Felder auf seine Weise (`publiziertab` oder `publiziert_ab`, `beschrieb` oder `beschreibung`, `plname_de` oder `name_de`). In der Demo stammen sie aus den INTERLIS-VIEW: Wer eine VIEW ändert, ändert den Dienst, ohne weiteren Code. Ein Client, der von einem Dienst zum anderen wechselt, muss seine Feldzuordnung neu erstellen.
- **Auch die Aufteilung in Collections unterscheidet sich.** geodienste.ch trennt die Energieformen in eigene Objektarten; die Demo fasst sie zusammen und unterscheidet sie über ein Attribut.
- **Die Ausdehnung ist nicht dieselbe.** geodienste.ch bündelt mehrere Kantone in einem Dienst; die Demo veröffentlicht jeweils einen kantonalen Datensatz.
- **Das Koordinatensystem wird unterschiedlich behandelt.** geodienste.ch arbeitet in EPSG:2056 und verlangt `crs` bei der OGC API; die Demo speichert in EPSG:2056, antwortet standardmässig in CRS84 und akzeptiert `crs` und `bbox-crs`.
- **Die Demo bietet Funktionen, die die verglichenen Dienste nicht haben**: JSON-FG, Queryables und Schema, OGC-API-Maps-Karten. Umgekehrt bieten die öffentlichen Dienste WMS, WFS und die Abdeckung zahlreicher Kantone.
- **Die Darstellung folgt unterschiedlichen Wegen.** Die WMS-Layer kommen vom Herausgeber bereits gezeichnet an; in der Demo stammt der Stil aus der in INTERLIS beschriebenen Darstellung, und das über OGC API - Features empfangene Objekt trägt keinen Stil.
