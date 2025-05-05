from nqs_bench_chem.core.molecule import build_molecule
from nqs_bench_chem.core.config import Experiment


def test_lih_scf_and_yaml():
    exp = Experiment.load("src/nqs_bench_chem/conf/lih_scan.yml")
    assert exp.system == "LiH"
    _, mf = build_molecule(exp.system, exp.basis_set)
    # crude energy sanity check
    assert abs(mf.e_tot) > 7.0
