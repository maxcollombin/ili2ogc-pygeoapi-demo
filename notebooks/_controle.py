"""Contrôle des notebooks, utilisé par run_all.sh.

`preparer SRC DST` : écrit dans DST une copie `solutions_NN_*.ipynb` de chaque notebook où chaque cellule « solution » est placée
juste après la cellule « exercice » de même rang, donc avant sa vérification.
`verifier-vierges DIR` : sur les notebooks exécutés sans solution, la première erreur de chacun doit venir
d'une cellule de vérification (un exercice non fait échoue à la vérification, pas ailleurs).
"""

import sys
from pathlib import Path

import nbformat


def etiquettes(cellule):
    return set(cellule.metadata.get("tags", []))


def preparer(src, dst):
    dst.mkdir(parents=True, exist_ok=True)
    for chemin in sorted(src.glob("[0-9][0-9]_*.ipynb")):
        nb = nbformat.read(chemin, as_version=4)
        origine = list(nb.cells)
        exercices = [c for c in origine if "exercice" in etiquettes(c)]
        solutions = [c for c in origine if "solution" in etiquettes(c)]
        assert len(exercices) == len(solutions), f"{chemin.name} : {len(exercices)} exercices, {len(solutions)} solutions"
        cellules = [c for c in origine if "solution" not in etiquettes(c)]
        # la n-ième solution remplace la n-ième cellule d'exercice : elle est placée juste après, avant la vérification
        for exercice, solution in reversed(list(zip(exercices, solutions))):
            cellules.insert(cellules.index(exercice) + 1, solution)
        nb.cells = cellules
        nbformat.write(nb, dst / f"solutions_{chemin.name}")
        print("solutions placées :", chemin.name)


def verifier_vierges(dossier):
    echecs = 0
    for chemin in sorted(dossier.glob("*.ipynb")):
        nb = nbformat.read(chemin, as_version=4)
        premiere = next(
            (
                c
                for c in nb.cells
                if c.cell_type == "code"
                and any(o.output_type == "error" for o in c.outputs)
            ),
            None,
        )
        if premiere is None:
            print(
                f"ECHEC {chemin.name} : aucune vérification n'échoue sans les solutions"
            )
            echecs += 1
        elif "verification" not in etiquettes(premiere):
            print(
                f"ECHEC {chemin.name} : première erreur hors vérification :\n{premiere.source[:200]}"
            )
            echecs += 1
        else:
            print(
                f"ok {chemin.name} : la première erreur vient d'une vérification, sans solution"
            )
    return echecs


if __name__ == "__main__":
    commande, *arguments = sys.argv[1:]
    if commande == "preparer":
        preparer(Path(arguments[0]), Path(arguments[1]))
    elif commande == "verifier-vierges":
        sys.exit(1 if verifier_vierges(Path(arguments[0])) else 0)
    else:
        sys.exit(f"commande inconnue : {commande}")
