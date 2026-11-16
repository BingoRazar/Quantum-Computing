
from qiskit import QuantumCircuit


def apply_oracle(qc, marked_state):
    """
    Flip the phase of the specified marked state.
    """

    n = len(marked_state)
   
    for qubit in range(n):
        if marked_state[n - 1 - qubit] == "0":
            qc.x(qubit)

    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)

    for qubit in range(n):
        if marked_state[n - 1 - qubit] == "0":
            qc.x(qubit)


def apply_diffusion(qc, n):
    """
    Apply Grover's diffusion operator.
    """

    qc.h(range(n))
    qc.x(range(n))

    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)

    qc.x(range(n))
    qc.h(range(n))


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

    qc.h(range(num_qubits))

    for _ in range(iterations):
        apply_oracle(qc, marked_state)
        apply_diffusion(qc, num_qubits)

    return qc
