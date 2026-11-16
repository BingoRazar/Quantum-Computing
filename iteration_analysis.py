
import math
import matplotlib.pyplot as plt

from qiskit.quantum_info import Statevector
from grover import build_grover_circuit


def theoretical_optimum(n):
    N = 2 ** n
    theta = math.asin(1 / math.sqrt(N))

    return round(math.pi / (4 * theta) - 0.5)


def analyse_iterations(n, marked):
    optimum = theoretical_optimum(n)

    # Test zero iterations and several iterations beyond the optimum.
    max_iterations = optimum + 4

    iterations = []
    probabilities = []

    for k in range(max_iterations + 1):
        qc = build_grover_circuit(n, marked, k)

        state = Statevector.from_instruction(qc)
        probability = state.probabilities_dict().get(marked, 0.0)

        iterations.append(k)
        probabilities.append(probability)

    print(f"\nQubits: {n}")
    print(f"Marked state: {marked}")
    print(f"Theoretical optimum: {optimum}")
    print(f"Empirically best iteration: {iterations[probabilities.index(max(probabilities))]}")

    for k, probability in zip(iterations, probabilities):
        print(f"Iterations: {k} | Success probability: {probability:.6f}")

    return iterations, probabilities, optimum


# Run experiments for 2, 3 and 4 qubits.
experiments = [
    (2, "11"),
    (3, "111"),
    (4, "1111")
]

plt.figure(figsize=(10, 6))

for n, marked in experiments:
    iterations, probabilities, optimum = analyse_iterations(n, marked)

    plt.plot(
        iterations,
        probabilities,
        marker="o",
        label=f"{n} qubits (optimum = {optimum})"
    )

plt.xlabel("Grover iterations")
plt.ylabel("Ideal marked-state probability")
plt.title("Grover Search: Success Probability vs Iterations")
plt.xticks(range(0, 9))
plt.ylim(0, 1.05)
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig("results/grover_iteration_analysis.png", dpi=300)
plt.show()
