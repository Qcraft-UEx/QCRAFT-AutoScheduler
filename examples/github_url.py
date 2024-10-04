from autoscheduler import Autoscheduler

# Create an instance of the Autoscheduler class
autoscheduler = Autoscheduler()

print("----------------AWS------------------")
# Define the circuit, the number of shots, and the maximum number of qubits
shots = 5000
circuit = "https://raw.githubusercontent.com/jorgecs/pythonscripts/main/shor7xMOD15Circuit.py"
max_qubits = 16

# Schedule the circuit inferring the qubits from the machine
scheduled_circuit, shots,times = autoscheduler.schedule(circuit, shots, machine='local')

# Execute the scheduled circuit
results = autoscheduler.execute(scheduled_circuit,shots,'local',times)
print(results)


print("----------------IBM------------------")
# Define the circuit, the number of shots, and the maximum number of qubits
circuit = "https://raw.githubusercontent.com/jorgecs/CompositionCircuits/main/simon.py"
shots = 5000
max_qubits = 29

# Schedule the circuit but this time using max_qubits instead of inferring from the machine
scheduled_circuit, shots, times = autoscheduler.schedule(circuit, shots, max_qubits=max_qubits)

# Execute the scheduled circuit
results = autoscheduler.execute(scheduled_circuit,shots,'local',times)
print(results)


# In the next example we will show how to use schedule_and_execute
print("----------------IBM schedule and execute------------------")
circuit = "https://raw.githubusercontent.com/jorgecs/CompositionCircuits/main/simon.py"
shots = 5000
results = autoscheduler.schedule_and_execute(circuit, shots, machine='local')
print(results)

# If we use max_qubits, it wont be inferred from the machine
print("----------------AWS schedule and execute------------------")
circuit = "https://raw.githubusercontent.com/jorgecs/pythonscripts/main/shor7xMOD15Circuit.py"
shots = 5000
results = autoscheduler.schedule_and_execute(circuit, shots, machine='local', max_qubits=8)
print(results)