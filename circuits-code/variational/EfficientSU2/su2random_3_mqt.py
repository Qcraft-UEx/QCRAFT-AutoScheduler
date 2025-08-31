from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as np

qreg_q = QuantumRegister(3, 'q')
creg_meas = ClassicalRegister(3, 'meas')
circuit = QuantumCircuit(qreg_q, creg_meas)

# Benchmark was created by MQT Bench on 2024-03-18
# For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
# MQT Bench version: 1.1.0
# Qiskit version: 1.0.2
circuit.u(1.4368347742816616, 1.563280899135842, -np.pi, qreg_q[0])
circuit.u(0.13038834331032637, 3.1322119352256292, 0, qreg_q[1])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.u(2.301856027570534, -1.7291536732871133, -np.pi, qreg_q[2])
circuit.cx(qreg_q[0], qreg_q[2])
circuit.u(1.2444656817555668, 0.5550554224571163, 0, qreg_q[0])
circuit.cx(qreg_q[1], qreg_q[2])
circuit.u(1.5046299106322627, 1.1646500873100205, -np.pi, qreg_q[1])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.u(1.062554723574571, -0.2928382424047804, 0, qreg_q[2])
circuit.cx(qreg_q[0], qreg_q[2])
circuit.u(0.02480768898038398, -2.434570523812673, 0, qreg_q[0])
circuit.cx(qreg_q[1], qreg_q[2])
circuit.u(3.0649864034230183, 1.3933297522764283, -np.pi, qreg_q[1])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.u(1.1773372206208805, -1.3076812305427237, -np.pi, qreg_q[2])
circuit.cx(qreg_q[0], qreg_q[2])
circuit.u(0.5166404252966228, -2.248311899378857, -np.pi, qreg_q[0])
circuit.cx(qreg_q[1], qreg_q[2])
circuit.u(1.793373244068875, -0.7958234754631421, -np.pi, qreg_q[1])
circuit.u(2.8742785055981956, 1.0941137716709264, -np.pi, qreg_q[2])
circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2])
circuit.measure(qreg_q[0], creg_meas[0])
circuit.measure(qreg_q[1], creg_meas[1])