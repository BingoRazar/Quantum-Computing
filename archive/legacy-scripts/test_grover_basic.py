
from qiskit.quantum_info import Statevector
from grover import build_grover_circuit

# Test different marked states.
tests = [
    (2, "10", 1),
    (3, "101", 2),
    (4, "0110", 3),
]

for n, marked, iterations in tests:

    qc = build_grover_circuit(n, marked, iterations)

    state = Statevector.from_instruction(qc)
    probabilities = state.probabilities_dict()

    success_probability = probabilities.get(marked, 0)

    print(f"\nQubits: {n}")
    print(f"Marked state: {marked}")
    print(f"Iterations: {iterations}")
    print(f"Success probability: {success_probability:.6f}")
