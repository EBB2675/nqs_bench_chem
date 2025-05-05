from .active_space import ActiveSpaceAdvisor
from .config import Experiment


def make_active_space(exp: Experiment):
    advisor = ActiveSpaceAdvisor(exp.selector)
    return advisor.select(exp.system, exp.basis_set, exp.qubit_budget)
