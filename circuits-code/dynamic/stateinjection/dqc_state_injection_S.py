from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from numpy import pi

qreg = QuantumRegister(2, 'q')
creg = ClassicalRegister(2, 'c')
circuit = QuantumCircuit(qreg, creg)

circuit.h(qreg[0])
circuit.h(qreg[0])
circuit.cx(qreg[0], qreg[1])
circuit.measure(qreg[1], creg[1])
circuit.z(qreg[0]).c_if(creg[1], 1)