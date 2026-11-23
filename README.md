# Grover's Algorithm: Implementation and Experimental Analysis

## Overview

This repository contains a modular implementation and experimental analysis of Grover's quantum search algorithm using Qiskit.

The project investigates the relationship between Grover iterations and search success probability, validates the implementation across different numbers of qubits and marked states, and records both ideal statevector probabilities and finite-shot measurement results.

The current implementation supports 2-, 3-, and 4-qubit search circuits.

## Project Structure

```text
qiskit-research/
├── archive/
│   ├── legacy-scripts/
│   └── legacy-results/
├── examples/
│   └── statevector_demo.py
├── experiments/
│   └── iteration_analysis.py
├── results/
│   ├── raw/
│   ├── processed/
│   └── figures/
├── src/
│   └── grover/
│       ├── __init__.py
│       ├── circuit.py
│       ├── oracle.py
│       ├── diffusion.py
│       └── simulation.py
├── tests/
│   ├── test_all_2q_targets.py
│   ├── test_grover.py
│   └── test_representative_targets.py
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

### Main components

- `circuit.py`: Constructs Grover search circuits.
- `oracle.py`: Implements the phase oracle for a specified marked state.
- `diffusion.py`: Implements the Grover diffusion operator.
- `simulation.py`: Provides ideal probability calculations, measurement simulation, and Wilson confidence intervals.
- `iteration_analysis.py`: Analyses success probability across different Grover iteration counts and generates experimental data and figures.
- `tests/`: Contains basic correctness tests and validation across different marked states.
- `examples/`: Contains a standalone statevector demonstration.
- `archive/`: Preserves earlier implementations and historical experimental outputs.

## Environment

The project was developed and tested using:

| Component | Version |
|---|---|
| Python | 3.14.7 |
| Qiskit | 2.5.2 |
| Qiskit Aer | 0.17.2 |
| NumPy | 2.5.4 |
| SciPy | 1.18.1 |
| Matplotlib | 3.11.2 |

Python requirement declared in `pyproject.toml`: Python 3.10 or newer.

Dependencies are pinned in both `pyproject.toml` and `requirements.txt`.

## Installation

Clone the repository and navigate into its directory.

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

Install the project in editable mode:

```powershell
python -m pip install -e .
```

Editable installation allows the `grover` package to be imported directly from the `src/` directory.

## Running the Tests

Run the test suite from the repository root:

```powershell
python -m unittest discover -s tests -v
```

The tests cover circuit behaviour, probability normalisation, oracle correctness, iteration effects, and representative marked states.

## Running the Iteration Analysis

Execute:

```powershell
python .\experiments\iteration_analysis.py
```

The experiment analyses Grover search for:

| Qubits | Marked states |
|---|---|
| 2 | `00`, `11` |
| 3 | `001`, `111` |
| 4 | `0110`, `1111` |

The analysis calculates ideal probabilities using Qiskit's statevector simulator and performs finite-shot simulations using Qiskit Aer.

Measurement experiments use 1,024 and 4,096 shots.

### Generated outputs

- `results/raw/iteration_experiment.csv`: Raw experimental records, including theoretical probabilities, observed probabilities, and confidence intervals.
- `results/figures/grover_iteration_analysis_targets.png`: Plot comparing ideal success probabilities across iteration counts and marked states.
- `results/processed/`: Reserved for processed experimental data and summaries.

The CSV currently contains 84 experimental records.

## Measurement and Bit Ordering

Marked states are represented as binary strings.

Qiskit uses little-endian qubit indexing: qubit 0 is the least significant bit, while displayed measurement bitstrings place the highest-index classical bit on the left.

The oracle accounts for this ordering when applying the phase flip. Measurements map qubits to classical bits using:

```python
measured.measure(range(n), range(n))
```

This ensures the returned measurement bitstrings correspond to the marked-state strings used by the experiment.

## Experimental Results

The implementation has been validated across all 2-qubit marked states and representative 3- and 4-qubit marked states.

For the representative experiments:

- 2 qubits: theoretical optimum of 1 Grover iteration.
- 3 qubits: theoretical optimum of 2 Grover iterations.
- 4 qubits: theoretical optimum of 3 Grover iterations.

The 3-qubit experiment with marked state `111` and 2 iterations produced an observed success rate of approximately 95.14% over 4,096 shots.

The 4-qubit experiment with marked state `0110` and 3 iterations produced an ideal success probability of approximately 96.13%.

## Current Status and Next Milestone

The current milestone establishes a modular, reproducible Grover implementation with validated behaviour and iteration-analysis experiments.

The next milestone is topology-aware transpilation.

The planned investigation will compare:

- Unrestricted transpilation.
- All-to-all connectivity.
- Star connectivity.
- Linear connectivity.

The investigation will examine 3- and 4-qubit circuits, using multiple transpiler seeds to evaluate variation in compiled circuit depth, gate counts, two-qubit gate counts, SWAP overhead, and compilation time.

The objective is to investigate how hardware connectivity constraints affect the compiled resource requirements of Grover circuits.

## Reproducibility

To reproduce the current experiments:

1. Use the pinned dependency versions.
2. Install the package in editable mode.
3. Run the test suite.
4. Execute the iteration-analysis script.
5. Inspect the generated CSV and figures in `results/`.

The repository preserves earlier implementations and historical outputs in `archive/` for reference.