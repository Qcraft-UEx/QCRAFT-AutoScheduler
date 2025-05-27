<p align="center">
   <picture>
     <source media="(prefers-color-scheme: dark)" srcset="https://github.com/Qcraft-UEx/Qcraft/blob/main/docs/_images/qcraft_logo.png?raw=true" width="60%">
     <img src="https://github.com/Qcraft-UEx/Qcraft/blob/main/docs/_images/qcraft_logo.png?raw=true" width="60%" alt="Qcraft Logo">
   </picture>
</p>

# QCRAFT AutoScheduler
[![PyPI Version](https://img.shields.io/pypi/v/autoscheduler.svg)](https://pypi.org/project/autoscheduler/)
![Python Versions](https://img.shields.io/badge/python-3.9%20|%203.10%20|%203.11%20|%203.12-blue.svg)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/Qcraft-UEx/QCRAFT/blob/main/LICENSE)

QCRAFT AutoScheduler: a library that allows users to automatically schedule the execution of their own quantum circuits, improving efficiency and reducing execution times in quantum computing environments. With this library, your Qiskit or Braket quantum circuit will be modified to increase its length but also decreasing the number of shots needed to execute it, getting a new circuit that needs more qubits but less shots to get the same result as the original circuit.

## Installation

You can install QCRAFT AutoScheduler and all its dependencies using pip:

```bash
pip install autoscheduler
```

You can also install from source by cloning the repository and installing from source:

```bash
git clone https://github.com/Qcraft-UEx/QCRAFT-AutoScheduler.git
cd autoscheduler
pip install .
```

## Usage

Here is a basic example on how to use AutoScheduler with a Quirk URL, when using a Quirk URL, it is mandatory to include the provider ('ibm' or 'aws') as an input.
```python
from autoscheduler import Autoscheduler

circuit = "https://algassert.com/quirk#circuit={'cols':[['H'],['•','X'],['Measure','Measure']]}"
max_qubits = 4
shots = 100
provider = 'ibm'
autoscheduler = Autoscheduler()
scheduled_circuit, shots, times = autoscheduler.schedule(circuit, shots, max_qubits=max_qubits, provider=provider)
results = autoscheduler.execute(scheduled_circuit,shots,'local',times)
```

Here is a basic example on how to use Autoscheduler with a GitHub URL.
```python
from autoscheduler import Autoscheduler

circuit = "https://raw.githubusercontent.com/user/repo/branch/file.py"
max_qubits = 15
shots = 1000
autoscheduler = Autoscheduler()
scheduled_circuit, shots, times = autoscheduler.schedule(circuit, shots, max_qubits=max_qubits)
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
autoscheduler = Autoscheduler()
scheduled_circuit, shots, times = autoscheduler.schedule(circuit, shots, max_qubits=max_qubits)
results = autoscheduler.execute(scheduled_circuit,shots,machine,times)
```

Here is a basic example on how to use Autoscheduler with a Qiskit circuit.
```python
from autoscheduler import Autoscheduler
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

qreg_q = QuantumRegister(4, 'q')
creg_c = ClassicalRegister(4, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)
circuit.h(qreg_q[1])
circuit.h(qreg_q[2])
circuit.h(qreg_q[3])
circuit.h(qreg_q[0])
circuit.ccx(qreg_q[1], qreg_q[0], qreg_q[3])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
circuit.cx(qreg_q[1], qreg_q[2])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2], qreg_q[3])
circuit.measure(qreg_q[1], creg_c[1])
circuit.measure(qreg_q[0], creg_c[0])
circuit.measure(qreg_q[2], creg_c[2])
circuit.measure(qreg_q[3], creg_c[3])

max_qubits = 127
shots = 2000
autoscheduler = Autoscheduler()
scheduled_circuit, shots, times = autoscheduler.schedule(circuit, shots, max_qubits=max_qubits)
results = autoscheduler.execute(scheduled_circuit,shots,machine,times)
```

It it possible to use the method schedule_and_execute instead of schedule and then execute, this method needs to have the machine in which you want to execute the circuit as a mandatory input. If the execution is on a aws machine, it is needed to specify the s3 bucket too. Also, provider is only needed when using Quirk URLs.

```python
from autoscheduler import Autoscheduler

circuit = "https://algassert.com/quirk#circuit={"cols":[["H","H","H"],["•","•",1,"X"],["•","X"],[1,"•","•","X"],[1,"•","X"],["•","X"],["Measure"],[1,"Measure"],[1,1,"Measure"],[1,1,1,"Measure"]]}"
max_qubits = 4
shots = 2000
provider = 'aws'
autoscheduler = Autoscheduler()
results = autoscheduler.schedule_and_execute(circuit, shots, 'ionq', max_qubits=max_qubits, provider=provider, s3_bucket=('amazon-braket-s3' 'my_braket_results'))
```

```python
from autoscheduler import Autoscheduler

circuit = "https://raw.githubusercontent.com/user/repo/branch/file.py"
max_qubits = 15
shots = 1000
autoscheduler = Autoscheduler()
results = autoscheduler.schedule_and_execute(circuit, shots, 'ibm_brisbane', max_qubits=max_qubits)
```

```python
from autoscheduler import Autoscheduler
from braket.circuits import Circuit

circuit = Circuit()
circuit.x(0)
circuit.cnot(0,1)

max_qubits = 8
shots = 300
autoscheduler = Autoscheduler()
results = autoscheduler.schedule_and_execute(circuit, shots, 'ionq', max_qubits=max_qubits, s3_bucket=('amazon-braket-s3' 'my_braket_results'))
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
autoscheduler = Autoscheduler()
results = autoscheduler.schedule_and_execute(circuit, shots, 'ibm_brisbane', max_qubits=max_qubits)

```

In schedule and schedule and execute you can use the machine to infer the value of max_qubits. It is mandatory to use at least one of those parameters to build the scheduled circuit.

```python
from autoscheduler import Autoscheduler
from braket.circuits import Circuit

circuit = Circuit()
circuit.x(0)
circuit.cnot(0,1)

max_qubits = 8
shots = 300
autoscheduler = Autoscheduler()
scheduled_circuit, shots, times = autoscheduler.schedule(circuit, shots, machine='local')
results = autoscheduler.execute(scheduled_circuit,shots,'local',times)

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
autoscheduler = Autoscheduler()
results = autoscheduler.schedule_and_execute(circuit, shots, 'ibm_brisbane')

```
QCRAFT AutoScheduler will utilize the default AWS and IBM Cloud credentials stored on the machine for cloud executions.

## Optimizing Quantum Tasks
This library aims for the shot optimization on quantum tasks. Reducing the cost of the circuit on the end-user.

### Shot optimization
To achieve the shot optimization, the original circuit will be composed multiple time with itself. The more segments, the less shots will be needed to replicate the original circuit.
The total number of shots may differ from the original on a very small scale because the library combines the original circuit multiple times. Depending on the maximum number of qubits, to achieve the desired number of shots and cost reduction the algorithm will create segments equal to the original circuit each with a proportional number of shots, all this on a unique circuit.

**Example:**
Consider a circuit with 2 qubits, requiring 100 shots. If the maximum number of qubits of the new scheduled circuit is 6, the shots will be reduced to 100/(6/2) = 34 in total. Upon uncheduling, the results of each segment of the circuit will be aggregated, resulting on 34*(6/2) = 102 shots in total. Even so, the cost reduction has been achieved because the number of shots has been reduced from 100 to 34.

## Changelog
The changelog is available [here](https://github.com/Qcraft-UEx/QCRAFT-AutoSchedulQ/blob/main/CHANGELOG.md)

## License
QCRAFT AutoScheduler is licensed under the [MIT License](https://github.com/Qcraft-UEx/QCRAFT/blob/main/LICENSE)
