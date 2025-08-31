from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as np

qreg = QuantumRegister(5, 'q')  # Single quantum register
creg = ClassicalRegister(4, 'c')  # Single classical register
circuit = QuantumCircuit(qreg, creg)

circuit.h(qreg[0])
circuit.h(qreg[1])
circuit.h(qreg[2])
circuit.h(qreg[3])
circuit.cp(np.pi / 512, qreg[3], qreg[4])
circuit.cp(np.pi / 256, qreg[2], qreg[4])
circuit.cp(np.pi / 128, qreg[1], qreg[4])
circuit.cp(np.pi / 64, qreg[0], qreg[4])
circuit.h(qreg[0])
circuit.measure(qreg[0], creg[0])
circuit.p(-np.pi / 2, qreg[1]).c_if(creg[0], 1)
circuit.p(-np.pi / 4, qreg[2]).c_if(creg[0], 1)
circuit.p(-np.pi / 8, qreg[3]).c_if(creg[0], 1)
circuit.h(qreg[1])
circuit.measure(qreg[1], creg[1])
circuit.p(-np.pi / 2, qreg[2]).c_if(creg[1], 1)
circuit.p(-np.pi / 4, qreg[3]).c_if(creg[1], 1)
circuit.h(qreg[2])
circuit.measure(qreg[2], creg[2])
circuit.p(-np.pi / 2, qreg[3]).c_if(creg[2], 1)
circuit.h(qreg[3])
circuit.measure(qreg[3], creg[3])