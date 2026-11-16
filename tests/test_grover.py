
import unittest
import numpy as np

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from grover import (
    build_grover_circuit,
    apply_oracle,
    apply_diffusion
)


class TestGrover(unittest.TestCase):

    # 1. Test every possible 2-qubit marked state.
    def test_all_two_qubit_targets(self):

        targets = ["00", "01", "10", "11"]

        for marked in targets:
            with self.subTest(marked=marked):

                qc = build_grover_circuit(2, marked, 1)
                state = Statevector.from_instruction(qc)

                probability = state.probabilities_dict()[marked]

                self.assertAlmostEqual(probability, 1.0, places=10)

    # 2. Test representative 3-qubit and 4-qubit targets.
    def test_representative_targets(self):

        tests = [
            (3, ["000", "001", "101", "111"], 2, 0.9453125),
            (4, ["0000", "0001", "0110", "1011", "1111"],
             3, 0.9613189697)
        ]

        for n, targets, iterations, expected in tests:

            for marked in targets:
                with self.subTest(n=n, marked=marked):

                    qc = build_grover_circuit(n, marked, iterations)
                    state = Statevector.from_instruction(qc)

                    probability = state.probabilities_dict()[marked]

                    self.assertAlmostEqual(
                        probability, expected, places=8
                    )

    # 3. Test invalid marked-state lengths and characters.
    def test_invalid_marked_states(self):

        with self.assertRaises(ValueError):
            build_grover_circuit(3, "10", 2)

        with self.assertRaises(ValueError):
            build_grover_circuit(3, "10A", 2)

        with self.assertRaises(ValueError):
            build_grover_circuit(3, "1 1", 2)

        with self.assertRaises(ValueError):
            build_grover_circuit(1, "1", 1)

    # 4. Test zero Grover iterations.
    def test_zero_iterations(self):

        n = 3
        marked = "101"

        qc = build_grover_circuit(n, marked, 0)
        state = Statevector.from_instruction(qc)

        probabilities = state.probabilities_dict()

        for probability in probabilities.values():
            self.assertAlmostEqual(probability, 1 / 8, places=10)

    # 5. Test that probabilities sum to one.
    def test_probability_normalisation(self):

        configurations = [
            (2, "10", 1),
            (3, "101", 2),
            (4, "0110", 3)
        ]

        for n, marked, iterations in configurations:
            with self.subTest(n=n):

                qc = build_grover_circuit(n, marked, iterations)
                state = Statevector.from_instruction(qc)

                total_probability = sum(state.probabilities())

                self.assertAlmostEqual(
                    total_probability, 1.0, places=10
                )

    # 6. Test that changing the iteration count changes the result.
    def test_iteration_count_changes_probability(self):

        n = 3
        marked = "101"

        probabilities = []

        for iterations in [0, 1, 2, 3]:

            qc = build_grover_circuit(n, marked, iterations)
            state = Statevector.from_instruction(qc)

            probability = state.probabilities_dict()[marked]
            probabilities.append(probability)

        self.assertAlmostEqual(probabilities[0], 0.125, places=10)
        self.assertAlmostEqual(probabilities[2], 0.9453125, places=8)

        self.assertNotAlmostEqual(
            probabilities[0], probabilities[1], places=5
        )

    # 7. Verify that the oracle flips only the marked state's phase.
    def test_oracle_marks_intended_state(self):

        configurations = [
            (2, "10"),
            (3, "101"),
            (4, "0110")
        ]

        for n, marked in configurations:
            with self.subTest(n=n, marked=marked):

                qc = QuantumCircuit(n)
                qc.h(range(n))

                apply_oracle(qc, marked)

                state = Statevector.from_instruction(qc)

                expected = np.full(
                    2 ** n,
                    1 / np.sqrt(2 ** n),
                    dtype=complex
                )

                expected[int(marked, 2)] *= -1

                np.testing.assert_allclose(
                    state.data,
                    expected,
                    atol=1e-10
                )

    # 8. Verify the diffusion operator independently.
    def test_diffusion_operator(self):

        for n in [2, 3, 4]:
            with self.subTest(n=n):

                qc = QuantumCircuit(n)
                qc.h(range(n))

                apply_diffusion(qc, n)

                state = Statevector.from_instruction(qc)

                expected = np.full(
                    2 ** n,
                    -1 / np.sqrt(2 ** n),
                    dtype=complex
                )

                np.testing.assert_allclose(
                    state.data,
                    expected,
                    atol=1e-10
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
