
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(2)

qc.h(0)
qc.h(1)

print("STAGE 1: After Hadamard gates")
print(Statevector.from_instruction(qc).data)

qc.cz(0, 1)

print("\nSTAGE 2: After oracle")
print(Statevector.from_instruction(qc).data)

qc.h([0, 1])
qc.x([0, 1])
qc.cz(0, 1)
qc.x([0, 1])
qc.h([0, 1])

print("\nSTAGE 3: After diffusion")
print(Statevector.from_instruction(qc).data)

print("Number of qubits:", qc.num_qubits)
print("Circuit depth:", qc.depth())
print("Total gate count:", qc.size())
print("Gate counts by type:", qc.count_ops())

print("\nCircuit diagram:")
print(qc.draw())
