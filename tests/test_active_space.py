from nqs_bench_chem.core import make_active_space
from nqs_bench_chem.core.config import Experiment


def test_lih_active_space():
    exp = Experiment.load("src/nqs_bench_chem/conf/lih_scan.yml")
    orbitals = make_active_space(exp)
    # Expect 6 spin‑orbitals (=> 12 qubits) for LiH / sto‑3g / budget 12
    assert len(orbitals) == 6
