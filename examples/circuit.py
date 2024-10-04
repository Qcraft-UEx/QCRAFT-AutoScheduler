from autoscheduler import Autoscheduler
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from braket.circuits import Circuit

# Create an instance of the Autoscheduler class
autoscheduler = Autoscheduler()

print("----------------Circuit Object IBM------------------")
# Create a quantum circuit using Qiskit
qreg_q = QuantumRegister(2, 'q')
creg_c = ClassicalRegister(2, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)
circuit.rx(0.5, qreg_q[0])
circuit.rx(0.5, qreg_q[1])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.rx(0.5, qreg_q[1])
circuit.rx(0.5, qreg_q[0])
circuit.rx(0.5, qreg_q[1])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.rx(0.5, qreg_q[0])
circuit.measure(qreg_q[0], creg_c[0])
circuit.measure(qreg_q[1], creg_c[1])

# Set the number of shots and the maximum number of qubits
shots = 5000
max_qubits = 4

# Schedule the circuit inferring the qubits from the machine
circuit,shots,times = autoscheduler.schedule(circuit, shots, machine='local')

# Execute the scheduled circuit
results = autoscheduler.execute(circuit,shots,'local',times)
print(results)


print("----------------Circuit Object AWS------------------")
# Create a quantum circuit using Braket
circuit = Circuit()
circuit.x(0)
circuit.x(1)
circuit.x(2)
circuit.x(3)   
circuit.cnot(2,1)
circuit.cnot(1,2)
circuit.cnot(2,1)
circuit.cnot(1,0)
circuit.cnot(0,1)
circuit.cnot(1,0)
circuit.cnot(3,0)
circuit.cnot(0,3)
circuit.ccnot(3,0,1)  
circuit.rx(1,0)
circuit.cswap(0, 1, 2)
circuit.phaseshift(0,0.15)
circuit.cphaseshift10(0, 1, 0.15)
circuit.s([1, 2])
circuit.gpi2(0, 0.15)
circuit.yy(0, 1, 0.15)
circuit.ms(0, 1, 0.15, 0.15, 0.15)

# Set the number of shots and the maximum number of qubits
shots = 5000
max_qubits = 8

# Schedule the circuit but this time using max_qubits instead of inferring from the machine
scheduled_circuit, shots, times = autoscheduler.schedule(circuit, shots, max_qubits=max_qubits)

# Execute the scheduled circuit
results = autoscheduler.execute(scheduled_circuit,shots,'local',times)
print(results)


# In the next example we will show how to use schedule_and_execute
print("----------------IBM schedule and execute------------------")
qreg_q = QuantumRegister(2, 'q')
creg_c = ClassicalRegister(2, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)
circuit.rx(0.5, qreg_q[0])
circuit.measure(qreg_q[0], creg_c[0])
circuit.measure(qreg_q[1], creg_c[1])

shots = 5000
results = autoscheduler.schedule_and_execute(circuit, shots, machine='local')
print(results)

# If we use max_qubits, it wont be inferred from the machine
print("----------------AWS schedule and execute------------------")
circuit = Circuit()
circuit.x(0)
circuit.x(1)

shots = 5000
results = autoscheduler.schedule_and_execute(circuit, shots, machine='local', max_qubits=8)
print(results)