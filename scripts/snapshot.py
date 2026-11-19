#!/usr/bin/env python3
"""Save the answers of a running stack as static files, so the documentation site can show them without a server.

    docker compose up -d   # then, once the loader has finished:
    python scripts/snapshot.py [BASE_URL] [OUTPUT_DIR]

Defaults: http://localhost:5000 and documentation/snapshot. The files are what the API answered on the day: the
links inside them still name BASE_URL.
"""

import json
import sys
from pathlib import Path

import requests

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000").rstrip("/")
OUT = Path(sys.argv[2] if len(sys.argv) > 2 else "documentation/snapshot")
MAP = "bbox-crs=http://www.opengis.net/def/crs/EPSG/0/2056&width=600&height=450&f=png"


def save(path: str, url: str, *, binary: bool = False) -> bool:
    response = requests.get(url, timeout=60)
    if response.status_code != 200:
        print(f"skipped {url}: {response.status_code}")
        return False
    target = OUT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    if binary:
        target.write_bytes(response.content)
    else:
        target.write_text(json.dumps(response.json(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return True


def extent_lv95(name: str) -> tuple[float, float, float, float] | None:
    """The extent of a collection's first features in LV95, with a margin (the map endpoint wants a bbox in a CRS)."""
    crs = "http://www.opengis.net/def/crs/EPSG/0/2056"
    answer = requests.get(f"{BASE}/collections/{name}/items?limit=500&f=json&crs={crs}", timeout=120)
    xs: list[float] = []
    ys: list[float] = []

    def walk(node) -> None:
        if node and isinstance(node[0], (int, float)):
            xs.append(node[0])
            ys.append(node[1])
        else:
            for child in node:
                walk(child)

    for feature in answer.json().get("features", []) if answer.status_code == 200 else []:
        if feature.get("geometry"):
            walk(feature["geometry"]["coordinates"])
    if not xs:
        return None
    margin = max(max(xs) - min(xs), max(ys) - min(ys), 200) * 0.05
    return min(xs) - margin, min(ys) - margin, max(xs) + margin, max(ys) + margin


def main() -> None:
    save("landing.json", f"{BASE}/?f=json")
    save("conformance.json", f"{BASE}/conformance?f=json")
    collections = requests.get(f"{BASE}/collections?f=json", timeout=60).json()["collections"]
    save("collections.json", f"{BASE}/collections?f=json")
    for collection in collections:
        name = collection["id"]
        save(f"{name}/collection.json", f"{BASE}/collections/{name}?f=json")
        save(f"{name}/schema.json", f"{BASE}/collections/{name}/schema?f=json")
        save(f"{name}/queryables.json", f"{BASE}/collections/{name}/queryables?f=json")
        save(f"{name}/items.json", f"{BASE}/collections/{name}/items?limit=5&f=json")
        save(f"{name}/items.jsonfg.json", f"{BASE}/collections/{name}/items?limit=5&f=jsonfg")
        bbox = extent_lv95(name)
        if bbox:
            x0, y0, x1, y1 = bbox
            save(f"{name}/map.png", f"{BASE}/collections/{name}/map?bbox={x0},{y0},{x1},{y1}&{MAP}", binary=True)
    print(f"{len(collections)} collections saved in {OUT}")


if __name__ == "__main__":
    main()
