from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as np

qreg_q = QuantumRegister(3, 'q')
creg_meas = ClassicalRegister(3, 'meas')
circuit = QuantumCircuit(qreg_q, creg_meas)

# Benchmark was created by MQT Bench on 2024-03-18
# For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
# MQT Bench version: 1.1.0
# Qiskit version: 1.0.2
circuit.h(qreg_q[0])
circuit.h(qreg_q[1])
circuit.rzz(5.094008139994057, qreg_q[0], qreg_q[1])
circuit.h(qreg_q[2])
circuit.rzz(5.094008139994057, qreg_q[0], qreg_q[2])
circuit.rx(-6.860310317223841, qreg_q[0])
circuit.rzz(5.094008139994057, qreg_q[1], qreg_q[2])
circuit.rx(-6.860310317223841, qreg_q[1])
circuit.rzz(-5.141522309483603, qreg_q[0], qreg_q[1])
circuit.rx(-6.860310317223841, qreg_q[2])
circuit.rzz(-5.141522309483603, qreg_q[0], qreg_q[2])
circuit.rx(8.165927224507852, qreg_q[0])
circuit.rzz(-5.141522309483603, qreg_q[1], qreg_q[2])
circuit.rx(8.165927224507852, qreg_q[1])
circuit.rx(8.165927224507852, qreg_q[2])
circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2])
circuit.measure(qreg_q[0], creg_meas[0])
circuit.measure(qreg_q[1], creg_meas[1])
circuit.measure(qreg_q[2], creg_meas[2])