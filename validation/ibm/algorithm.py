from autoscheduler import Autoscheduler

circuit = "https://raw.githubusercontent.com/user/repo/branch/path/to/file.py"
shots = 10000
max_qubits = 127

#Schedule the circuit
autoscheduler = Autoscheduler()
scheduled_circuit, shots, times = autoscheduler.schedule(circuit, max_qubits, shots)
#Execute the scheduled circuit
results = autoscheduler.execute(scheduled_circuit,shots,'ibm_brisbane',times)
print(results)