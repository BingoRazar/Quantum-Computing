from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

qc = QuantumCircuit(3,3)
qc.h(0)
qc.h(1)
qc.h(2)
qc.measure(range(3), range(3))
simulator=AerSimulator()
result=simulator.run(qc,shots=1000, seed_simulator=42).result()
counts=result.get_counts()
