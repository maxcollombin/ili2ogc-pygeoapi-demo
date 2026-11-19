#!/usr/bin/env bash
# Exécute tous les notebooks de bout en bout, dans un environnement neuf.
#   1. copies avec les solutions : toutes les vérifications doivent passer ;
#   2. notebooks tels que livrés (sans solutions) : la première erreur doit venir d'une vérification.
# Les notebooks exécutés sont écrits dans le dossier donné en argument (par défaut /tmp/notebooks-controle).
# Demande Internet (fetch-models, pip), `uv` et, pour la fin du notebook 04, Docker (le port 5000 doit être libre ;
# la pile est arrêtée par le notebook). Les copies avec solutions (`solutions_NN_*.ipynb`) sont écrites à côté des
# notebooks, pour que les chemins relatifs (`../data`, `../collections`) restent valables ; elles sont supprimées à la fin.
set -euo pipefail

ICI="$(cd "$(dirname "$0")" && pwd)"
SORTIE="$(realpath -m "${1:-${TMPDIR:-/tmp}/notebooks-controle}")"
VENV="$SORTIE/venv"

rm -rf "$SORTIE/avec-solutions" "$SORTIE/sans-solutions" "$ICI"/solutions_*.ipynb "$ICI/modeles" "$ICI/sorties"
mkdir -p "$SORTIE"
[ -x "$VENV/bin/python" ] || uv venv --seed -q --python 3.12 "$VENV"
uv pip install -q --python "$VENV/bin/python" jupyter nbconvert ipykernel nbformat

export PATH="$VENV/bin:$PATH"
cd "$ICI"

"$VENV/bin/python" _controle.py preparer "$ICI" "$ICI"

echo "== 1/2 : notebooks avec solutions"
START=$(date +%s)
jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=900 \
  --output-dir "$SORTIE/avec-solutions" "$ICI"/solutions_[0-9][0-9]_*.ipynb
echo "durée : $(( $(date +%s) - START )) s"

rm -rf "$ICI/modeles" "$ICI/sorties"  # repartir de zéro : aucune sortie de la passe précédente
echo "== 2/2 : notebooks livrés, sans solutions (les vérifications doivent échouer)"
START=$(date +%s)
jupyter nbconvert --to notebook --execute --allow-errors --ExecutePreprocessor.timeout=900 \
  --output-dir "$SORTIE/sans-solutions" "$ICI"/[0-9][0-9]_*.ipynb
echo "durée : $(( $(date +%s) - START )) s"
"$VENV/bin/python" _controle.py verifier-vierges "$SORTIE/sans-solutions"

rm -rf "$ICI"/solutions_*.ipynb "$ICI/modeles" "$ICI/sorties"
echo "Tous les notebooks passent. Sorties dans $SORTIE"
