from autoscheduler import Autoscheduler

# Create an instance of the Autoscheduler class
autoscheduler = Autoscheduler()

print("----------------AWS------------------")
# Define the circuit, the number of shots, the maximum number of qubits and the provider
circuit = "https://algassert.com/quirk#circuit={'cols':[['H'],['•','X'],['Measure','Measure']]}"
shots = 5000
max_qubits = 4
provider = "aws"

# Schedule the circuit
scheduled_circuit, shots, times = autoscheduler.schedule(circuit, max_qubits, shots, provider)

# Execute the scheduled circuit
results = autoscheduler.execute(scheduled_circuit,shots,'local',times)
print(results)


print("----------------IBM------------------")
# Define the circuit, the number of shots, the maximum number of qubits and the provider
circuit = "https://algassert.com/quirk#circuit={'cols':[['H'],['•','X'],['Measure','Measure']]}"
shots = 2500
machine = "local"
max_qubits = 4
provider = 'ibm'

# Schedule the circuit
scheduled_circuit, shots, times = autoscheduler.schedule(circuit, max_qubits, shots, provider)

# Execute the scheduled circuit
result = autoscheduler.execute(scheduled_circuit,shots,'local', times)
print(result)