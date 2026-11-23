
import math

from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

from .circuit import build_grover_circuit


def wilson_interval(successes, shots, z=1.96):
    """
    Calculate the Wilson confidence interval for a measured
    success probability.

    z=1.96 corresponds approximately to a 95% confidence interval.
    """

    if shots <= 0:
        raise ValueError("Shots must be greater than zero.")

    if successes < 0 or successes > shots:
        raise ValueError("Successes must be between zero and shots.")

    p = successes / shots

    denominator = 1 + z**2 / shots

    centre = (
        p + z**2 / (2 * shots)
    ) / denominator

    margin = (
        z * math.sqrt(
            p * (1 - p) / shots
            + z**2 / (4 * shots**2)
        )
        / denominator
    )

    return centre - margin, centre + margin


def ideal_probabilities(num_qubits, marked_state, iterations):
    """
    Calculate ideal measurement probabilities using a statevector.
    """

    circuit = build_grover_circuit(
        num_qubits,
        marked_state,
        iterations
    )

    state = Statevector.from_instruction(circuit)

    return state.probabilities_dict()


def simulate_measurements(
    num_qubits,
    marked_state,
    iterations,
    shots=4096,
    seed=42
):
    """
    Simulate Grover's algorithm using Qiskit Aer.

    Returns the observed success probability, confidence interval,
    and measurement counts.
    """

    if shots <= 0:
        raise ValueError("Shots must be greater than zero.")

    logical = build_grover_circuit(
        num_qubits,
        marked_state,
        iterations
    )

    # Create a separate circuit for measurements.
    measured = QuantumCircuit(num_qubits, num_qubits)

    measured.compose(logical, inplace=True)
    measured.measure(range(num_qubits), range(num_qubits))

    simulator = AerSimulator()

    compiled = transpile(measured, simulator)

    result = simulator.run(
        compiled,
        shots=shots,
        seed_simulator=seed
    ).result()

    counts = result.get_counts()

    successes = counts.get(marked_state, 0)

    probability = successes / shots

    lower, upper = wilson_interval(successes, shots)

    return {
        "probability": probability,
        "confidence_interval": (lower, upper),
        "counts": counts,
        "shots": shots
    }
