ARG PYGEOAPI_VERSION=0.24.0
FROM geopython/pygeoapi:${PYGEOAPI_VERSION}

# pygeoapi-plugins is installed without its dependencies (geopandas, pyarrow, numpy ...: about 500 MB). Only its JSON-FG
# formatter is used, and that one needs pygeoapi alone; the package's formatter/__init__ imports every formatter, so it
# is cut down to that one.
RUN /venv/bin/python3 -m pip install --no-cache-dir psycopg2-binary \
 && /venv/bin/python3 -m pip install --no-cache-dir --no-deps pygeoapi-plugins \
 && PLUGINS="$(/venv/bin/python3 -c 'import importlib.util as u; print(list(u.find_spec("pygeoapi_plugins").submodule_search_locations)[0])')" \
 && printf 'from pygeoapi_plugins.formatter.jsonfg import JSONFGFormatter as JSONFG\n' > "$PLUGINS/formatter/__init__.py"

# JSON-FG formatter of this demo: pygeoapi_plugins' one, with `featureType` = the VIEW a collection serves, not
# `OGRGeoJSON`. Put next to the installed packages so the configuration can name it as `ili2ogc_jsonfg.JSONFG`.
COPY ili2ogc_jsonfg.py /tmp/ili2ogc_jsonfg.py
RUN cp /tmp/ili2ogc_jsonfg.py "$(/venv/bin/python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')/" \
 && rm /tmp/ili2ogc_jsonfg.py

COPY pygeoapi-config.yml /pygeoapi/local.config.yml
