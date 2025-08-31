from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as np

qreg_q = QuantumRegister(5, 'q')
creg_meas = ClassicalRegister(5, 'meas')
circuit = QuantumCircuit(qreg_q, creg_meas)

# Benchmark was created by MQT Bench on 2024-03-19
# For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
# MQT Bench version: 1.1.0
# Qiskit version: 1.0.2
circuit.ry(-2.399967605019755, qreg_q[0])
circuit.ry(-0.003596948684433063, qreg_q[1])
circuit.ry(2.314018886718823, qreg_q[2])
circuit.ry(-0.10853420674224268, qreg_q[3])
circuit.ry(2.345026373859055, qreg_q[4])
circuit.cx(qreg_q[3], qreg_q[4])
circuit.cx(qreg_q[2], qreg_q[3])
circuit.cx(qreg_q[1], qreg_q[2])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.ry(0.9240833542270186, qreg_q[0])
circuit.ry(-1.0994127158439237, qreg_q[1])
circuit.ry(-1.655777277088476, qreg_q[2])
circuit.ry(-1.6856866830091894, qreg_q[3])
circuit.ry(-0.7725696035849275, qreg_q[4])
circuit.cx(qreg_q[3], qreg_q[4])
circuit.cx(qreg_q[2], qreg_q[3])
circuit.cx(qreg_q[1], qreg_q[2])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.ry(2.03112411886031, qreg_q[0])
circuit.ry(2.4246203197554133, qreg_q[1])
circuit.ry(1.5673757927308016, qreg_q[2])
circuit.ry(-2.8076832584951785, qreg_q[3])
circuit.ry(-1.6463357401948455, qreg_q[4])
circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2], qreg_q[3], qreg_q[4])
circuit.measure(qreg_q[0], creg_meas[0])
circuit.measure(qreg_q[1], creg_meas[1])
circuit.measure(qreg_q[2], creg_meas[2])
circuit.measure(qreg_q[3], creg_meas[3])
circuit.measure(qreg_q[4], creg_meas[4])