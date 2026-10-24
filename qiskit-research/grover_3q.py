from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
import math

n = 3
marked = "1" * n
iterations = math.floor((math.pi / 4) * math.sqrt(2**n))

qc = QuantumCircuit(n, n)

qc.h(range(n))

# Grover iterations
for _ in range(iterations):
    # Oracle: mark |111>
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)

    # Diffusion operator
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    qc.x(range(n))
    qc.h(range(n))

logical = qc.remove_final_measurements(inplace=False)

state = Statevector.from_instruction(logical)
probabilities = state.probabilities_dict()

print("\nIdeal probabilities:")
for bitstring, probability in sorted(probabilities.items()):
    print(f"{bitstring}: {probability:.6f}")

# Logical circuit metrics (exclude measurements)
print("\nCircuit metrics:")
print("Number of qubits:", logical.num_qubits)
print("Logical depth:", logical.depth())
print("Logical gate count:", logical.size())
print("Gate counts:", logical.count_ops())

# Finite-shot simulation
measured = logical.copy()
measured.measure_all()

simulator = AerSimulator()
result = simulator.run(measured, shots=4096, seed_simulator=42).result()
counts = result.get_counts()

print("\nMeasurement counts:")
print(counts)

marked_frequency = counts.get(marked + " 000", 0) / 4096
print("Marked-state frequency:", marked_frequency)