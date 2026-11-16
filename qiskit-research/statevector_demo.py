
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

qc = QuantumCircuit(3)
qc.h(0)
qc.h(1)
qc.h(2)
state = Statevector.from_instruction(qc)
probabilities = state.probabilities_dict()
print("Ideal probabilities:")
print(probabilities)
measured_qc = QuantumCircuit(3, 3)
measured_qc.h(0)
measured_qc.h(1)
measured_qc.h(2)
measured_qc.measure(range(3), range(3))
simulator = AerSimulator()
result = simulator.run(
    measured_qc,
    shots=1000,
    seed_simulator=42
).result()
counts = result.get_counts()
print("\nFinite-shot counts:")
print(counts)
print("\nObserved frequencies:")
for outcome, count in sorted(counts.items()):
    print(f"{outcome}: {count / 1000:.3f}")
