from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as np

qreg = QuantumRegister(3, 'q')  
creg_meas = ClassicalRegister(3, 'meas')
circuit = QuantumCircuit(qreg, creg_meas)

# Benchmark fue creado por MQT Bench el 2024-03-19
# Para más información sobre MQT Bench, visite https://www.cda.cit.tum.de/mqtbench/
# Versión MQT Bench: 1.1.0
# Versión Qiskit: 1.0.2

circuit.h(qreg[2])  
circuit.ccx(qreg[2], qreg[1], qreg[0])  
circuit.cx(qreg[2], qreg[1])  
circuit.x(qreg[1]) 
circuit.x(qreg[2])  
circuit.ccx(qreg[2], qreg[1], qreg[0])  
circuit.cx(qreg[2], qreg[1])  
circuit.x(qreg[1])  
circuit.u(np.pi / 2, -np.pi, -np.pi, qreg[2])  
circuit.ccx(qreg[2], qreg[1], qreg[0])  
circuit.cx(qreg[2], qreg[1])  
circuit.x(qreg[1])  
circuit.x(qreg[2])  
circuit.ccx(qreg[2], qreg[1], qreg[0])  
circuit.cx(qreg[2], qreg[1])  
circuit.x(qreg[1])  
circuit.u(np.pi / 2, -np.pi, -np.pi, qreg[2])  
circuit.ccx(qreg[2], qreg[1], qreg[0])  
circuit.cx(qreg[2], qreg[1]) 
circuit.x(qreg[1])  
circuit.x(qreg[2])  
circuit.ccx(qreg[2], qreg[1], qreg[0])  
circuit.cx(qreg[2], qreg[1])  
circuit.x(qreg[1])  
circuit.x(qreg[2])  


circuit.barrier(qreg[0], qreg[1], qreg[2])


circuit.measure(qreg[0], creg_meas[0])  
circuit.measure(qreg[1], creg_meas[1])  
circuit.measure(qreg[2], creg_meas[2])  