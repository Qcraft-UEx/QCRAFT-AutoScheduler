from autoscheduler import Autoscheduler

# Create an instance of the Autoscheduler class
autoscheduler = Autoscheduler()

print("----------------AWS------------------")
# Define the circuit, the number of shots, and the maximum number of qubits
shots = 5000
circuit = "https://raw.githubusercontent.com/jorgecs/pythonscripts/main/shor7xMOD15Circuit.py"
max_qubits = 16

# Schedule the circuit
scheduled_circuit, shots,times = autoscheduler.schedule(circuit, max_qubits, shots)

# Execute the scheduled circuit
results = autoscheduler.execute(scheduled_circuit,shots,'local',times)
print(results)


print("----------------IBM------------------")
# Define the circuit, the number of shots, and the maximum number of qubits
circuit = "https://raw.githubusercontent.com/jorgecs/CompositionCircuits/main/simon.py"
shots = 5000
max_qubits = 29

# Schedule the circuit
scheduled_circuit, shots, times = autoscheduler.schedule(circuit, max_qubits, shots)

# Execute the scheduled circuit
results = autoscheduler.execute(scheduled_circuit,shots,'local',times)
print(results)