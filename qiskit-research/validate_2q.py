
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

qc = QuantumCircuit(2, 2)

qc.h([0, 1])
qc.cz(0, 1)

# Diffusion
qc.h([0, 1])
qc.x([0, 1])
qc.cz(0, 1)
qc.x([0, 1])
qc.h([0, 1])

ideal_state = Statevector.from_instruction(qc)
ideal_probabilities = ideal_state.probabilities_dict()

print("Ideal probabilities:")
print(ideal_probabilities)

# Add measurements
qc.measure([0, 1], [0, 1])

# Finite-shot validation
simulator = AerSimulator()
result = simulator.run(
    qc,
    shots=4096,
    seed_simulator=42
).result()

counts = result.get_counts()
print("\nFinite-shot counts:")
print(counts)

marked = "11"
frequency = counts.get(marked, 0) / 4096
print(f"\nFrequency of marked state: {frequency:.4f}")
