<p align="center">
   <picture>
     <source media="(prefers-color-scheme: dark)" srcset="https://github.com/Qcraft-UEx/Qcraft/blob/main/docs/_images/qcraft_logo.png?raw=true" width="60%">
     <img src="https://github.com/Qcraft-UEx/Qcraft/blob/main/docs/_images/qcraft_logo.png?raw=true" width="60%" alt="Qcraft Logo">
   </picture>
  </a>
</p>


# QCRAFT AutoSchedulQ

## Description

QCRAFT AutoSchedulQ: a library that allows users to automatically schedule the execution of their own quantum circuits, improving efficiency and reducing execution times in quantum computing environments. With this library, your Qiskit or Braket quantum circuit will be modified to increase its length but also decreasing the number of shots needed to execute it, getting a new circuit that needs more qubits but less shots to get the same result as the original circuit.

## Installation

You can install QCRAFT AutoSchedulQ and all its dependencies using pip:

```bash
pip install autoscheduler
```

You can also install from source by cloning the repository and installing from source:

```bash
git clone https://github.com/Qcraft-UEx/QCRAFT-AutoSchedulQ.git
cd autoscheduler
pip install .
```

## Usage

Here is a basic example on how to use Autoscheduler with a Quirk URL, when using a Quirk URL, it is mandatory to include the provider ('ibm' or 'aws') as an input.
```python
from autoscheduler import Autoscheduler

circuit = "https://algassert.com/quirk#circuit={'cols':[['H'],['•','X'],['Measure','Measure']]}"
max_qubits = 4
shots = 100
provider = 'ibm'
autoscheduler = Autoscheduler()
scheduled_circuit, shots, times = autoscheduler.schedule(circuit, max_qubits, shots, provider)
results = autoscheduler.execute(scheduled_circuit,shots,'local',times)
```

Here is a basic example on how to use Autoscheduler with a GitHub URL.
```python
from autoscheduler import Autoscheduler

circuit = "https://raw.githubusercontent.com/user/repo/branch/file.py"
max_qubits = 15
shots = 1000
autoscheduler = Autoscheduler()
scheduled_circuit, shots, times = autoscheduler.schedule(circuit, max_qubits, shots)
results = autoscheduler.execute(scheduled_circuit,shots,'local',times)
```

Here is a basic example on how to use Autoscheduler with a Braket circuit.
```python
from autoscheduler import Autoscheduler
from braket.circuits import Circuit

circuit = Circuit()
circuit.x(0)
circuit.cnot(0,1)

max_qubits = 8
shots = 300
scheduled_circuit, shots, times = autoscheduler.schedule(circuit, max_qubits, shots)
results = autoscheduler.execute(scheduled_circuit,shots,'local',times)
```

Here is a basic example on how to use Autoscheduler with a Qiskit circuit.
```python
from autoscheduler import Autoscheduler
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

qreg_q = QuantumRegister(2, 'q')
creg_c = ClassicalRegister(2, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)
circuit.h(qreg_q[0])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.measure(qreg_q[0], creg_c[0])
circuit.measure(qreg_q[1], creg_c[1])

max_qubits = 16
shots = 500
scheduled_circuit, shots, times = autoscheduler.schedule(circuit, max_qubits, shots)
results = autoscheduler.execute(scheduled_circuit,shots,'local',times)
```

It it possible to use the method schedule_and_execute instead of schedule and then execute, this method needs to have the machine in which you want to execute the circuit as a mandatory input. If the execution is on a aws machine, it is needed to specify the s3 bucket too. Also, provider is only needed when using Quirk URLs.

```python
from autoscheduler import Autoscheduler

circuit = "https://algassert.com/quirk#circuit={'cols':[['H'],['•','X'],['Measure','Measure']]}"
max_qubits = 4
shots = 100
provider = 'aws'
autoscheduler = Autoscheduler()
results = autoscheduler.schedule_and_execute(circuit, max_qubits, shots, 'ionq', provider, 'amazon-braket-s3')
```

```python
from autoscheduler import Autoscheduler

circuit = "https://raw.githubusercontent.com/user/repo/branch/file.py"
max_qubits = 15
shots = 1000
autoscheduler = Autoscheduler()
results = autoscheduler.schedule_and_execute(circuit, max_qubits, shots, 'ibm_brisbane')
```

```python
from autoscheduler import Autoscheduler
from braket.circuits import Circuit

circuit = Circuit()
circuit.x(0)
circuit.cnot(0,1)

max_qubits = 8
shots = 300
results = autoscheduler.schedule_and_execute(circuit, max_qubits, shots, 'ionq', s3_bucket='amazon-braket-s3')
```

```python
from autoscheduler import Autoscheduler
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

qreg_q = QuantumRegister(2, 'q')
creg_c = ClassicalRegister(2, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)
circuit.h(qreg_q[0])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.measure(qreg_q[0], creg_c[0])
circuit.measure(qreg_q[1], creg_c[1])

max_qubits = 16
shots = 500
results = autoscheduler.schedule_and_execute(circuit, max_qubits, shots, 'ibm_brisbane')

```

## License
Autoscheduler is licensed under the [MIT License](LICENSE)

