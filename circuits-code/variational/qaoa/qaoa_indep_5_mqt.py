from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as np

qreg_q = QuantumRegister(5, 'q')
creg_meas = ClassicalRegister(5, 'meas')
circuit = QuantumCircuit(qreg_q, creg_meas)

# Benchmark was created by MQT Bench on 2024-03-18
# For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
# MQT Bench version: 1.1.0
# Qiskit version: 1.0.2
circuit.h(qreg_q[0])
circuit.h(qreg_q[1])
circuit.rzz(-1.930004982171882, qreg_q[0], qreg_q[1])
circuit.h(qreg_q[2])
circuit.rzz(-1.930004982171882, qreg_q[0], qreg_q[2])
circuit.rx(-2.6436411784439646, qreg_q[0])
circuit.h(qreg_q[3])
circuit.rzz(-1.930004982171882, qreg_q[1], qreg_q[3])
circuit.rx(-2.6436411784439646, qreg_q[1])
circuit.rzz(-3.639726195721819, qreg_q[0], qreg_q[1])
circuit.h(qreg_q[4])
circuit.rzz(-1.930004982171882, qreg_q[2], qreg_q[4])
circuit.rx(-2.6436411784439646, qreg_q[2])
circuit.rzz(-3.639726195721819, qreg_q[0], qreg_q[2])
circuit.rx(1.9303385045328598, qreg_q[0])
circuit.rzz(-1.930004982171882, qreg_q[3], qreg_q[4])
circuit.rx(-2.6436411784439646, qreg_q[3])
circuit.rzz(-3.639726195721819, qreg_q[1], qreg_q[3])
circuit.rx(1.9303385045328598, qreg_q[1])
circuit.rx(-2.6436411784439646, qreg_q[4])
circuit.rzz(-3.639726195721819, qreg_q[2], qreg_q[4])
circuit.rx(1.9303385045328598, qreg_q[2])
circuit.rzz(-3.639726195721819, qreg_q[3], qreg_q[4])
circuit.rx(1.9303385045328598, qreg_q[3])
circuit.rx(1.9303385045328598, qreg_q[4])
circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2], qreg_q[3], qreg_q[4])
circuit.measure(qreg_q[0], creg_meas[0])
circuit.measure(qreg_q[1], creg_meas[1])
circuit.measure(qreg_q[2], creg_meas[2])
circuit.measure(qreg_q[3], creg_meas[3])
circuit.measure(qreg_q[4], creg_meas[4])