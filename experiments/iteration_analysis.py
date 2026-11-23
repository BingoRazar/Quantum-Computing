
import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt

from grover import (
    ideal_probabilities,
    simulate_measurements,
)


# Resolve paths relative to the repository root.
ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = ROOT / "results" / "raw"
FIGURES_DIR = ROOT / "results" / "figures"


def theoretical_optimum(n):
    N = 2 ** n
    theta = math.asin(1 / math.sqrt(N))

    return round(math.pi / (4 * theta) - 0.5)


def analyse_iterations(n, marked):
    optimum = theoretical_optimum(n)
    max_iterations = optimum + 2

    iterations = []
    probabilities = []

    for k in range(max_iterations + 1):

        distribution = ideal_probabilities(n, marked, k)
        probability = distribution.get(marked, 0.0)

        iterations.append(k)
        probabilities.append(probability)

    best_iteration = iterations[probabilities.index(max(probabilities))]

    print(f"\nQubits: {n}")
    print(f"Marked state: {marked}")
    print(f"Theoretical optimum: {optimum}")
    print(f"Empirically best iteration: {best_iteration}")

    for k, probability in zip(iterations, probabilities):
        print(f"Iterations: {k} | Success probability: {probability:.6f}")

    return iterations, probabilities, optimum


def plot_iteration_analysis():

    experiments = [
        (2, ["00", "11"]),
        (3, ["001", "111"]),
        (4, ["0110", "1111"])
    ]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=True)

    for ax, (n, targets) in zip(axes, experiments):

        optimum = theoretical_optimum(n)

        for marked in targets:

            iterations, probabilities, _ = analyse_iterations(n, marked)

            ax.plot(
                iterations,
                probabilities,
                marker="o",
                label=f"Target {marked}"
            )

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

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    filename = FIGURES_DIR / "grover_iteration_analysis_targets.png"

    plt.savefig(filename, dpi=300)
    print(f"\nSaved figure to {filename}")

    plt.show()
    plt.close(fig)


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

                distribution = ideal_probabilities(
                    n, marked, iterations
                )

                theoretical_probability = distribution.get(marked, 0.0)

                for shots in shots_list:

                    result = simulate_measurements(
                        n,
                        marked,
                        iterations,
                        shots=shots
                    )

                    lower, upper = result["confidence_interval"]

                    rows.append({
                        "qubits": n,
                        "marked_state": marked,
                        "iterations": iterations,
                        "shots": shots,
                        "theoretical_probability": theoretical_probability,
                        "observed_probability": result["probability"],
                        "ci_lower": lower,
                        "ci_upper": upper
                    })

    return rows


def save_results(rows):

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    filename = RAW_DIR / "iteration_experiment.csv"

    fieldnames = rows[0].keys()

    with open(filename, "w", newline="") as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSaved {len(rows)} experiments to {filename}")


def main():

    plot_iteration_analysis()

    n = 3
    marked = "111"
    iterations = 2

    for shots in [1024, 4096]:

        result = simulate_measurements(
            n,
            marked,
            iterations,
            shots=shots
        )

        lower, upper = result["confidence_interval"]

        print(f"\nShots: {shots}")
        print(f"Observed success rate: {result['probability']:.4f}")
        print(f"95% confidence interval: [{lower:.4f}, {upper:.4f}]")

    rows = generate_experiment_data()
    save_results(rows)


if __name__ == "__main__":
    main()
