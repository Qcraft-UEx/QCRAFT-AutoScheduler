<p align="center">
   <picture>
     <source media="(prefers-color-scheme: dark)" srcset="https://github.com/Qcraft-UEx/Qcraft/blob/main/docs/_images/qcraft_logo.png?raw=true" width="60%">
     <img src="https://github.com/Qcraft-UEx/Qcraft/blob/main/docs/_images/qcraft_logo.png?raw=true" width="60%" alt="Qcraft Logo">
   </picture>
</p>

# QCRAFT AutoScheduler: Automated Quantum Circuit Scheduling
[![PyPI Version](https://img.shields.io/pypi/v/autoscheduler.svg)](https://pypi.org/project/autoscheduler/)
![Python Versions](https://img.shields.io/badge/python-3.9%20|%203.10%20|%203.11%20|%203.12%20|%203.13-blue.svg)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/Qcraft-UEx/QCRAFT/blob/main/LICENSE)

The **QCRAFT AutoScheduler** is a developer-oriented library designed to **automatically schedule quantum circuits** by replicating them to maximize the utilization of available qubits on a quantum processor. This novel approach improves efficiency, substantially **reduces execution costs and waiting times**, and optimizes hardware usage in Noisy Intermediate-Scale Quantum (NISQ) computing environments.

The library achieves this by transforming a source circuit into a **composite circuit** with greater width and a proportionally **reduced number of measurement shots**. This process effectively multiplexes multiple instances of the original quantum task into a single, more resource-efficient.

---

## AutoScheduler Process Overview

The autoscheduling process is a four-step pipeline that automatically handles the composition, execution, and reconstruction of results for quantum circuits. 

<p align="center">
   <picture>
     <source media="(prefers-color-scheme: dark)" srcset="https://github.com/Qcraft-UEx/QCRAFT-AutoScheduler/blob/main/autoscheduler/Autoscheduler_imagen.png?raw=true" width="60%">
     <img src="https://github.com/Qcraft-UEx/QCRAFT-AutoScheduler/blob/main/autoscheduler/Autoscheduler_imagen.png?raw=true" width="35%" alt="QCRAFT AutoScheduler">
   </picture>
</p>

1. **Scheduling (Autoscheduling):** The library takes the user's quantum circuit ($C$) and the maximum available qubits ($q_{max}$) as input. It then calculates how many replicas ($r$) of the circuit can fit onto the quantum processor and generates a new, wider composite circuit ($C'$). The total required shots ($s$) are divided proportionally among the replicas, reducing the number of shots required for the single execution of $C'$.
2. **Execution (Quantum Execution):** The composite circuit ($C'$) is submitted as a single task to the selected quantum computer or simulator (QPU). This execution has a lower shot count, which directly reduces the execution time and cost compared to executing the original circuit sequentially $r$ times.
3. **Unscheduling:** After the execution completes, the Unscheduler method is responsible for reconstructing the distribution of the results of the original circuit. It reconstructs the original circuit's result distribution by aggregating the outcomes from all replicas. This is achieved by performing an arithmetic sum of the frequencies obtained for each specific result across all segments.
4. **Results:** The final output delivered to the developer is the reconstructed result distribution, equivalent to having executed the original circuit with the full, initial shot count.

---
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

---

## Usage

Here is a basic example on how to use AutoScheduler with a Quirk URL, when using a Quirk URL, it is mandatory to include the provider ('ibm' or 'aws') as an input.
```python
# Import Autoscheduler library
from autoscheduler import Autoscheduler

# Circuit initialization (Bell State): loaded from Quirk visual tool
circuit = "https://algassert.com/quirk#circuit={'cols':[['H'],['•','X'],['Measure','Measure']]}"

# Configuration: define shots, backend and qubit constraints
max_qubits = 4
shots = 100
provider = 'ibm'

# Scheduler initialization and circuit scheduling
autoscheduler = Autoscheduler()
scheduled_circuit, shots, times = autoscheduler.schedule(
    circuit, shots, max_qubits=max_qubits, provider=provider)

# Execution of scheduled circuit on a simulator (or backend)
results = autoscheduler.execute(scheduled_circuit, shots, 'local', times)

```

Here is a basic example on how to use Autoscheduler with a GitHub URL.
```python
# Import Autoscheduler library
from autoscheduler import Autoscheduler

# Circuit loaded from raw GitHub file
circuit = "https://raw.githubusercontent.com/user/repo/branch/file.py"

# Configuration: define shots and qubit constraints
max_qubits = 15
shots = 1000

# Scheduler initialization and circuit scheduling
autoscheduler = Autoscheduler()
scheduled_circuit, shots, times = autoscheduler.schedule(circuit, shots, max_qubits=max_qubits)
results = autoscheduler.execute(scheduled_circuit,shots,'local',times)
```

Here is a basic example on how to use Autoscheduler with a Braket circuit.
```python
# Import Autoscheduler library and neccesary Braket libraries
from autoscheduler import Autoscheduler
from braket.circuits import Circuit

# Circuit definition using Braket SDK
circuit = Circuit()
circuit.x(0)
circuit.cnot(0,1)

# Configuration and scheduling
max_qubits = 8
shots = 300
autoscheduler = Autoscheduler()
scheduled_circuit, shots, times = autoscheduler.schedule(circuit, shots, max_qubits=max_qubits)
results = autoscheduler.execute(scheduled_circuit,shots,machine,times)
```

Here is a basic example on how to use Autoscheduler with a Qiskit circuit.
```python

# Import Autoscheduler library and neccesary Qiskit libraries
from autoscheduler import Autoscheduler
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

# Full Adder circuit creation with 4 qubits and measurement
qreg_q = QuantumRegister(4, 'q')
creg_c = ClassicalRegister(4, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

# Add gates and barrier
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

# Configuration: define shots and qubit constraints
max_qubits = 127
shots = 2000

# Scheduler initialization and circuit scheduling
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

# Circuit definition
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

# Circuit definition
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

# Circuit definition
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

# Circuit definition
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

---

## Quantum Task Optimization
The core objective of the AutoScheduler is shot optimization, which reduces the task execution cost for the end-user.

### Shot Reduction Mechanism
To achieve the shot optimization, the original circuit will be composed multiple time with itself. The more segments, the less shots will be needed to replicate the original circuit.
The total number of shots may differ from the original on a very small scale because the library combines the original circuit multiple times. Depending on the maximum number of qubits, to achieve the desired number of shots and cost reduction the algorithm will create segments equal to the original circuit each with a proportional number of shots, all this on a unique circuit.

**Example:**
A circuit requiring 1000 shots on 4 qubits, running on a 20-qubit processor ($q_{max}=20$), will be replicated 5 times.
- Original Circuit Shots: 1000
- Replication Factor: $20 \text{ qubits} / 4 \text{ qubits} = 5$
- Composite Circuit Shots: $1000 / 5 = 200$ shots.

The cost reduction achieved in validation experiments was 80.7% on Amazon Braket. The result aggregation during unscheduling recovers the statistical power equivalent to the original 1000 shots.


---

## Changelog
The changelog is available [here](https://github.com/Qcraft-UEx/QCRAFT-AutoScheduler/blob/main/CHANGELOG.md)

---

## License
QCRAFT AutoScheduler is licensed under the [MIT License](https://github.com/Qcraft-UEx/QCRAFT/blob/main/LICENSE)
