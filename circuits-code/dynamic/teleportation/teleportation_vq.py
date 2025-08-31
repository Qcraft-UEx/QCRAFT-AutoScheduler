from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as np

qreg_q = QuantumRegister(3, 'q')
creg_c = ClassicalRegister(3, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

circuit.h(qreg_q[2])
circuit.cx(qreg_q[2], qreg_q[1])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.h(qreg_q[0])
circuit.measure(qreg_q[1], creg_c[1])
circuit.x(qreg_q[2]).c_if(creg_c[1], 1)
circuit.measure(qreg_q[0], creg_c[0])
circuit.z(qreg_q[2]).c_if(creg_c[0], 1)
circuit.measure(qreg_q[2], creg_c[2])