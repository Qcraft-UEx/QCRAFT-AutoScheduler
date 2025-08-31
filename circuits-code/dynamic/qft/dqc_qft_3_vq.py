from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as  np

qreg_q = QuantumRegister(3, 'q')
creg_c = ClassicalRegister(1, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

circuit.h(qreg_q[0])
circuit.measure(qreg_q[0], creg_c[0])
circuit.p(np.pi / 2, qreg_q[1]).c_if(creg_c[0], 1)
circuit.p(np.pi / 4, qreg_q[2]).c_if(creg_c[0], 1)
circuit.h(qreg_q[1])
circuit.measure(qreg_q[1], creg_c[0])
circuit.p(np.pi / 2, qreg_q[2]).c_if(creg_c[0], 1)
circuit.h(qreg_q[2])
circuit.measure(qreg_q[2], creg_c[0])