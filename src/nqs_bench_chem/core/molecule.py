from __future__ import annotations
from pathlib import Path
from pyscf import gto, scf


def build_molecule(label_or_file: str, basis: str = "sto-3g"):
    """
    Accept 'LiH' / 'H2' strings *or* a path to an XYZ file.
    Returns (mol, mf) where mf is a converged RHF object.
    """
    if Path(label_or_file).is_file():
        atoms = str(Path(label_or_file).resolve())
    elif label_or_file.lower() == "lih":
        atoms = "Li 0 0 0; H 0 0 1.6"
    elif label_or_file.lower() == "h2":
        atoms = "H 0 0 0; H 0 0 0.74"
    else:
        raise ValueError(
            f"Unknown system '{label_or_file}'. Provide XYZ or extend templates."
        )

    mol = gto.M(atom=atoms, basis=basis, unit="Angstrom", symmetry=True, verbose=0)
    mf = scf.RHF(mol).run()
    return mol, mf
