from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute
from numpy import pi

qreg_q = QuantumRegister(2, 'q')
creg_c = ClassicalRegister(2, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

# Parameters
# First layer of mixing and cost Hamiltonian
circuit.rx(0.5, qreg_q[0])
circuit.rx(0.5, qreg_q[1])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.rx(0.5, qreg_q[1])
# Second layer of mixing and cost Hamiltonian
circuit.rx(0.5, qreg_q[0])
circuit.rx(0.5, qreg_q[1])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.rx(0.5, qreg_q[0])
# Measurement
circuit.measure(qreg_q[0], creg_c[0])
circuit.measure(qreg_q[1], creg_c[1])

backend = Aer.get_backend("qasm_simulator")
x=int(1024)
job = execute(circuit, backend, shots=x)
result = job.result()
counts = result.get_counts()
