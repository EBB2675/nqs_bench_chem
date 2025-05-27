import numpy as np
from qiskit.providers.aer.noise import (
    NoiseModel,
    depolarizing_error,
    amplitude_damping_error,
    thermal_relaxation_error,
    QuantumError,
)

def add_depolarizing(noise_model: NoiseModel,
                     p1: float, p2: float,
                     single_qubit_gates: list = ['u'],
                     two_qubit_gates: list = ['cx']) -> NoiseModel:
    """Add depolarizing error: p1 for 1-qubit, p2 for 2-qubit gates."""
    err1 = depolarizing_error(p1, 1)
    for g in single_qubit_gates:
        noise_model.add_all_qubit_quantum_error(err1, g)
    err2 = depolarizing_error(p2, 2)
    for g in two_qubit_gates:
        noise_model.add_all_qubit_quantum_error(err2, g)
    return noise_model


def add_amplitude_damping(noise_model: NoiseModel,
                          p_amp: float,
                          gates: list = ['u', 'cx']) -> NoiseModel:
    """Add amplitude-damping (T1) error with probability p_amp."""
    err = amplitude_damping_error(p_amp)
    for g in gates:
        noise_model.add_all_qubit_quantum_error(err, g)
    return noise_model


def add_thermal_relaxation(noise_model: NoiseModel,
                           t1: float, t2: float, gate_time: float,
                           gates: list = ['u', 'cx']) -> NoiseModel:
    """
    Add thermal relaxation (T1 & T2) error.
    gate_time in same units as t1/t2.
    """
    err1q = thermal_relaxation_error(t1, t2, gate_time, num_qubits=1)
    err2q = thermal_relaxation_error(t1, t2, gate_time, num_qubits=2)
    for g in gates:
        if g in ['cx', 'cz', 'swap']:
            noise_model.add_all_qubit_quantum_error(err2q, g)
        else:
            noise_model.add_all_qubit_quantum_error(err1q, g)
    return noise_model


def add_crosstalk(noise_model: NoiseModel,
                  p_corr: float,
                  qubit_pairs: list) -> NoiseModel:
    """
    Add correlated bit-flip (X⊗X) error of strength p_corr
    on the ‘id’ instruction for each (i,j) in qubit_pairs.
    """
    # Kraus ops: √(1−p) I⊗I, √p X⊗X
    K0 = np.sqrt(1 - p_corr) * np.eye(4)
    X2 = np.kron([[0,1],[1,0]], [[0,1],[1,0]])
    K1 = np.sqrt(p_corr) * X2
    error = QuantumError([K0, K1])
    for i, j in qubit_pairs:
        noise_model.add_quantum_error(error, ['id'], [(i, j)])
    return noise_model
