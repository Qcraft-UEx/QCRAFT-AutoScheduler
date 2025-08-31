from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as np

qreg_q = QuantumRegister(3, 'q')
creg_meas = ClassicalRegister(3, 'meas')
circuit = QuantumCircuit(qreg_q, creg_meas)

# Benchmark was created by MQT Bench on 2024-03-19
# For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
# MQT Bench version: 1.1.0
# Qiskit version: 1.0.2
circuit.ry(-0.9413251507535245, qreg_q[0])
circuit.ry(-0.12641277016975258, qreg_q[1])
circuit.ry(-np.pi, qreg_q[2])
circuit.cx(qreg_q[1], qreg_q[2])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.ry(-2.2065597028049257, qreg_q[0])
circuit.ry(-np.pi, qreg_q[1])
circuit.ry(1.749025192431949, qreg_q[2])
circuit.cx(qreg_q[1], qreg_q[2])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.ry(0.6901007506009792, qreg_q[0])
circuit.ry(-0.40245553923277066, qreg_q[1])
circuit.ry(2.7174409942016213, qreg_q[2])
circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2])
circuit.measure(qreg_q[0], creg_meas[0])
circuit.measure(qreg_q[1], creg_meas[1])
circuit.measure(qreg_q[2], creg_meas[2])