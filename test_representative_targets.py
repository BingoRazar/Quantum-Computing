
from qiskit.quantum_info import Statevector
from grover import build_grover_circuit

tests = [
    (3, ["000", "001", "101", "111"], 2, 0.9453125),
    (4, ["0000", "0001", "0110", "1011", "1111"], 3, 0.9613189697)
]

for n, targets, iterations, expected_probability in tests:

    print(f"\nTesting {n}-qubit targets")

    for marked in targets:

        qc = build_grover_circuit(n, marked, iterations)

        state = Statevector.from_instruction(qc)
        probabilities = state.probabilities_dict()

        success_probability = probabilities.get(marked, 0)

        print(
            f"Target: {marked} | "
            f"Success probability: {success_probability:.6f}"
        )

        assert abs(
            success_probability - expected_probability
        ) < 1e-8

print("\nAll representative target tests passed!")
