````markdown
# NQS Bench Chem

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> **Work in Progress**: This library is under active development. APIs and features may change.

A Python package for running noise-aware, active-space Variational Quantum Eigensolver (VQE) benchmarks on small molecular systems using tensor-network quantum states.

## Features

- Build and simulate VQE circuits with user-defined ansätze and active spaces
- Support for multiple noise models:
  - Depolarizing (1- and 2-qubit)
  - Amplitude damping (T1 relaxation)
  - Thermal relaxation (T1 & T2)
  - Crosstalk (correlated errors)
- Pluggable classical optimizers
- Customizable molecules and active-space selection
- Easy-to-extend API for new noise channels and backends

## Installation

```bash
# Clone the repository and install in editable (development) mode
git clone https://github.com/EBB2675/nqs_bench_chem.git
cd nqs_bench_chem
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
````

This will install the core dependencies and development tools (pytest, flake8, black).

## Quickstart

```python
from nqs_bench_chem.benchmark import run_benchmark
from nqs_bench_chem.noise_models import build_noise_model

# Define a noise configuration
noise_cfg = {
  'depol':     {'p1': 1e-3, 'p2': 1e-2},
  'amp':       {'p': 2e-3},
  'thermal':   {'t1': 5e4, 't2': 5e4, 'gate_time': 0.1},
  'crosstalk': {'p_corr': 1e-3, 'pairs': [[0,1], [1,2]]},
}

# Build noise model
noise_model = build_noise_model(noise_cfg)

# Run a VQE benchmark for H2 molecule
results = run_benchmark(
    molecule="H2",
    active_space=[0, 1],
    ansatz="hardware_efficient",
    noise_model=noise_model,
)

print(results)
```

## Development

* **Tests**: `pytest --maxfail=1 --disable-warnings -q`
* **Linting**: `black --check src tests && flake8`
* **Type checking**: `mypy src`

Contributions are welcome! Please open issues or pull requests.

```
```
