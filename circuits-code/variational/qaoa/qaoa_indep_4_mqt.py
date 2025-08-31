from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from numpy import pi

qreg_q = QuantumRegister(4, 'q')
creg_meas = ClassicalRegister(4, 'meas')
circuit = QuantumCircuit(qreg_q, creg_meas)

# Benchmark was created by MQT Bench on 2024-03-18
# For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
# MQT Bench version: 1.1.0
# Qiskit version: 1.0.2
circuit.h(qreg_q[0])
circuit.h(qreg_q[1])
circuit.rzz(-4.712387194486129, qreg_q[0], qreg_q[1])
circuit.h(qreg_q[2])
circuit.rzz(-4.712387194486129, qreg_q[0], qreg_q[2])
circuit.rx(8.63937561261258, qreg_q[0])
circuit.h(qreg_q[3])
circuit.rzz(-4.712387194486129, qreg_q[1], qreg_q[3])
circuit.rx(8.63937561261258, qreg_q[1])
circuit.rzz(0.785393361472697, qreg_q[0], qreg_q[1])
circuit.rzz(-4.712387194486129, qreg_q[2], qreg_q[3])
circuit.rx(8.63937561261258, qreg_q[2])
circuit.rzz(0.785393361472697, qreg_q[0], qreg_q[2])
circuit.rx(4.712387043046583, qreg_q[0])
circuit.rx(8.63937561261258, qreg_q[3])
circuit.rzz(0.785393361472697, qreg_q[1], qreg_q[3])
circuit.rx(4.712387043046583, qreg_q[1])
circuit.rzz(0.785393361472697, qreg_q[2], qreg_q[3])
circuit.rx(4.712387043046583, qreg_q[2])
circuit.rx(4.712387043046583, qreg_q[3])
circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2], qreg_q[3])
circuit.measure(qreg_q[0], creg_meas[0])
circuit.measure(qreg_q[1], creg_meas[1])
circuit.measure(qreg_q[2], creg_meas[2])
circuit.measure(qreg_q[3], creg_meas[3])