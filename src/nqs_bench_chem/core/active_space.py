from __future__ import annotations
from typing import List
import numpy as np
from pyscf import mp
from .molecule import build_molecule


class ActiveSpaceAdvisor:
    """Pick an active space that respects the qubit budget."""

    def __init__(self, selector: str = "noon"):
        if selector not in {"noon"}:
            raise ValueError(f"Unknown selector '{selector}'")
        self.selector = selector

    # ---------- public API ----------
    def select(self, system: str, basis: str, qubit_budget: int) -> List[int]:
        _, mf = build_molecule(system, basis)
        if self.selector == "noon":
            return self._select_noon(mf, qubit_budget)

    # ---------- implementation ----------
    @staticmethod
    def _select_noon(mf, qubit_budget: int) -> List[int]:
        """
        Use MP2 1‑RDM to obtain natural‑orbital occupations, rank by |n‑1|,
        and keep the first `qubit_budget // 2` *spatial* orbitals.
        """
        m2 = mp.MP2(mf).run()

        # 1 · spin‑summed 1‑RDM in AO basis
        dm_ao = m2.make_rdm1()

        # 2 · transform to MO basis
        C = mf.mo_coeff
        dm_mo = C.T @ dm_ao @ C  # (nmo, nmo)

        # 3 · natural occupations = diag of MO‑basis 1‑RDM
        noon = np.diag(dm_mo)  # values ~ 0‒2

        # 4 · rank by |n-1|
        order = np.argsort(np.abs(noon - 1.0))[::-1]

        n_pairs = qubit_budget // 2
        chosen = order[: 2 * n_pairs]  # top k spin‑orbitals
        return sorted(chosen.tolist())
