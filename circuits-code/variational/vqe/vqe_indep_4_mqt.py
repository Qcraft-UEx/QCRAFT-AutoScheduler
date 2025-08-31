from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as np

qreg_q = QuantumRegister(4, 'q')
creg_meas = ClassicalRegister(4, 'meas')
circuit = QuantumCircuit(qreg_q, creg_meas)

# Benchmark was created by MQT Bench on 2024-03-19
# For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
# MQT Bench version: 1.1.0
# Qiskit version: 1.0.2
circuit.ry(2.2550838042508814, qreg_q[0])
circuit.ry(-0.00024211540731557916, qreg_q[1])
circuit.ry(1.6710237090859774, qreg_q[2])
circuit.ry(-2.4683764674701445, qreg_q[3])
circuit.cx(qreg_q[2], qreg_q[3])
circuit.cx(qreg_q[1], qreg_q[2])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.ry(0.05242096891171133, qreg_q[0])
circuit.ry(0.06725228443923906, qreg_q[1])
circuit.ry(0.15986425080312602, qreg_q[2])
circuit.ry(-0.12427572772829466, qreg_q[3])
circuit.cx(qreg_q[2], qreg_q[3])
circuit.cx(qreg_q[1], qreg_q[2])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.ry(-2.253454955203389, qreg_q[0])
circuit.ry(-3.099043494910433, qreg_q[1])
circuit.ry(1.5706098165320757, qreg_q[2])
circuit.ry(2.462214751559368, qreg_q[3])
circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2], qreg_q[3])
circuit.measure(qreg_q[0], creg_meas[0])
circuit.measure(qreg_q[1], creg_meas[1])
circuit.measure(qreg_q[2], creg_meas[2])
circuit.measure(qreg_q[3], creg_meas[3])