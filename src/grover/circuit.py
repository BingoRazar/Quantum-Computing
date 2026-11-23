
from qiskit import QuantumCircuit

from .oracle import apply_oracle
from .diffusion import apply_diffusion


def build_grover_circuit(num_qubits, marked_state, iterations):
    """
    Construct a Grover search circuit.
    """

    if num_qubits < 2:
        raise ValueError("At least 2 qubits are required.")

    if len(marked_state) != num_qubits:
        raise ValueError("Marked state length must equal number of qubits.")

    if any(bit not in "01" for bit in marked_state):
        raise ValueError("Marked state must contain only 0s and 1s.")

    if iterations < 0:
        raise ValueError("Iterations cannot be negative.")

    qc = QuantumCircuit(num_qubits)

    # Initialise uniform superposition.
    qc.h(range(num_qubits))

    # Grover iterations.
    for _ in range(iterations):
        apply_oracle(qc, marked_state)
        apply_diffusion(qc, num_qubits)

    return qc
