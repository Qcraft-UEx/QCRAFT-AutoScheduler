from autoscheduler import Autoscheduler

# Create an instance of the Autoscheduler class
autoscheduler = Autoscheduler()

print("----------------AWS------------------")
# Define the circuit, the number of shots, the maximum number of qubits and the provider
circuit = "https://algassert.com/quirk#circuit={'cols':[['H'],['•','X'],['Measure','Measure']]}"
shots = 5000
max_qubits = 4
provider = "aws"

# Schedule the circuit inferring the qubits from the machine
scheduled_circuit, shots, times = autoscheduler.schedule(circuit, shots, machine='local', provider=provider)

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

# Schedule the circuit but this time using max_qubits instead of inferring from the machine
scheduled_circuit, shots, times = autoscheduler.schedule(circuit, shots, max_qubits=max_qubits, provider=provider)

# Execute the scheduled circuit
result = autoscheduler.execute(scheduled_circuit,shots,'local', times)
print(result)


# In the next example we will show how to use schedule_and_execute
print("----------------IBM schedule and execute------------------")
circuit = "https://algassert.com/quirk#circuit={'cols':[['H'],['•','X'],['Measure','Measure']]}"
shots = 5000
results = autoscheduler.schedule_and_execute(circuit, shots, machine='local', provider='ibm')
print(results)

# If we use max_qubits, it wont be inferred from the machine
print("----------------AWS schedule and execute------------------")
circuit = "https://algassert.com/quirk#circuit={'cols':[['H'],['•','X'],['Measure','Measure']]}"
shots = 5000
results = autoscheduler.schedule_and_execute(circuit, shots, machine='local', max_qubits=8, provider='aws')
print(results)