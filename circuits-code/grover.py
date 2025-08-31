from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import execute, Aer
from qiskit import transpile
from qiskit_ibm_provider import least_busy, IBMProvider
import numpy as np

qreg_q = QuantumRegister(2, 'q')
creg_c = ClassicalRegister(2, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

circuit.h(qreg_q[0])
circuit.h(qreg_q[1])
circuit.x(qreg_q[1])
circuit.h(qreg_q[1])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.h(qreg_q[1])
circuit.x(qreg_q[1])
circuit.h(qreg_q[1])
circuit.measure(qreg_q[0], creg_c[0])
circuit.measure(qreg_q[1], creg_c[1])

shots = 10000
provider = IBMProvider()
backend = Aer.get_backend('qasm_simulator')

qc_basis = transpile(circuit, backend)
job = execute(qc_basis, backend=backend, shots=shots)
job_result = job.result()
print(job_result.get_counts(qc_basis))
