
import math
import matplotlib.pyplot as plt
import csv

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

from qiskit.quantum_info import Statevector
from grover import build_grover_circuit


def theoretical_optimum(n):
    N = 2 ** n
    theta = math.asin(1 / math.sqrt(N))

    return round(math.pi / (4 * theta) - 0.5)


def wilson_interval(successes, shots, z=1.96):
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


def simulate_measurements(n, marked, iterations, shots, seed=42):
    logical = build_grover_circuit(n, marked, iterations)

    # Create a separate circuit for measurement.
    measured = QuantumCircuit(n, n)
    measured.compose(logical, inplace=True)
    measured.measure(range(n), range(n))

    simulator = AerSimulator()
    compiled = transpile(measured, simulator)

    result = simulator.run(
        compiled,
        shots=shots,
        seed_simulator=seed
    ).result()

    counts = result.get_counts()

    successes = counts.get(marked, 0)
    probability = successes / shots

    lower, upper = wilson_interval(successes, shots)

    return probability, lower, upper

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



# Test two different marked states for each problem size.
experiments = [
    (2, ["00", "11"]),
    (3, ["001", "111"]),
    (4, ["0110", "1111"])
]

# Create one graph for each problem size.
fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=True)

for ax, (n, targets) in zip(axes, experiments):

    optimum = theoretical_optimum(n)

    for marked in targets:

        iterations, probabilities, optimum = analyse_iterations(n, marked)

        ax.plot(
            iterations,
            probabilities,
            marker="o",
            label=f"Target {marked}"
        )

    # Mark the theoretical optimum.
    ax.axvline(
        optimum,
        linestyle="--",
        alpha=0.7,
        label=f"Theoretical optimum = {optimum}"
    )

    ax.set_title(f"{n} Qubits")
    ax.set_xlabel("Grover iterations")
    ax.set_ylim(0, 1.05)
    ax.grid(True)
    ax.legend()

axes[0].set_ylabel("Ideal marked-state probability")

fig.suptitle("Grover Search: Effect of Marked State and Iterations")
plt.tight_layout()

plt.savefig(
    "results/grover_iteration_analysis_targets.png",
    dpi=300
)

plt.show()

def generate_experiment_data():

    experiments = {
        2: ["00", "11"],
        3: ["001", "111"],
        4: ["0110", "1111"]
    }

    shots_list = [1024, 4096]

    rows = []

    for n, targets in experiments.items():

        optimum = theoretical_optimum(n)

        for marked in targets:

            for iterations in range(optimum + 5):

                qc = build_grover_circuit(n, marked, iterations)

                state = Statevector.from_instruction(qc)
                theoretical_probability = (
                    state.probabilities_dict().get(marked, 0.0)
                )

                for shots in shots_list:

                    observed, lower, upper = simulate_measurements(
                        n, marked, iterations, shots
                    )

                    rows.append({
                        "qubits": n,
                        "marked_state": marked,
                        "iterations": iterations,
                        "shots": shots,
                        "theoretical_probability": theoretical_probability,
                        "observed_probability": observed,
                        "ci_lower": lower,
                        "ci_upper": upper
                    })

    return rows
def save_results(rows):

    filename = "results/iteration_experiment.csv"

    fieldnames = rows[0].keys()

    with open(filename, "w", newline="") as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSaved {len(rows)} experiments to {filename}")
if __name__ == "__main__":
    n = 3
    marked = "111"
    iterations = 2

    for shots in [1024, 4096]:
        probability, lower, upper = simulate_measurements(
            n, marked, iterations, shots
        )

        print(f"\nShots: {shots}")
        print(f"Observed success rate: {probability:.4f}")
        print(f"95% confidence interval: [{lower:.4f}, {upper:.4f}]")
    rows = generate_experiment_data()
    save_results(rows)