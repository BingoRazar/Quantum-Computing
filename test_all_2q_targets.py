
from itertools import product

from qiskit.quantum_info import Statevector
from grover import build_grover_circuit

# Generate every possible 2-qubit marked state.
marked_states = [
    "".join(bits)
    for bits in product("01", repeat=2)
]

print("Testing all 2-qubit marked states\n")

for marked in marked_states:

    qc = build_grover_circuit(
        num_qubits=2,
        marked_state=marked,
        iterations=1
    )

    state = Statevector.from_instruction(qc)
    probabilities = state.probabilities_dict()

    success_probability = probabilities.get(marked, 0)

    print(
        f"Target: {marked} | "
        f"Success probability: {success_probability:.6f}"
    )

    assert abs(success_probability - 1.0) < 1e-10

print("\nAll 2-qubit target tests passed!")
