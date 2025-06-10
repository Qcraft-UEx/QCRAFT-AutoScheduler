.. _usage:

Usage
=====

Here is a basic example on how to use Autoscheduler with a Quirk URL. When using a Quirk URL, it is mandatory to include the provider ('ibm' or 'aws') as an input.

.. code-block:: python

    from autoscheduler import Autoscheduler

    circuit = "https://algassert.com/quirk#circuit={'cols':[['H'],['•','X'],['Measure','Measure']]}"
    max_qubits = 4
    shots = 100
    provider = 'ibm'
    autoscheduler = Autoscheduler()
    scheduled_circuit, shots, times = autoscheduler.schedule(circuit, shots, max_qubits=max_qubits, provider=provider)
    results = autoscheduler.execute(scheduled_circuit, shots, 'local', times)

Here is a basic example on how to use Autoscheduler with a GitHub URL.

.. code-block:: python

    from autoscheduler import Autoscheduler

    circuit = "https://raw.githubusercontent.com/user/repo/branch/file.py"
    max_qubits = 15
    shots = 1000
    autoscheduler = Autoscheduler()
    scheduled_circuit, shots, times = autoscheduler.schedule(circuit, shots, max_qubits=max_qubits)
    results = autoscheduler.execute(scheduled_circuit, shots, 'local', times)

Here is a basic example on how to use Autoscheduler with a Braket circuit.

.. code-block:: python

    from autoscheduler import Autoscheduler
    from braket.circuits import Circuit

    circuit = Circuit()
    circuit.x(0)
    circuit.cnot(0,1)

    max_qubits = 8
    shots = 300
    autoscheduler = Autoscheduler()
    scheduled_circuit, shots, times = autoscheduler.schedule(circuit, shots, max_qubits=max_qubits)
    results = autoscheduler.execute(scheduled_circuit, shots, 'local', times)

Here is a basic example on how to use Autoscheduler with a Qiskit circuit.

.. code-block:: python

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
    scheduled_circuit, shots, times = autoscheduler.schedule(circuit, shots, max_qubits=max_qubits)
    results = autoscheduler.execute(scheduled_circuit, shots, 'local', times)

It is possible to use the method `schedule_and_execute` instead of `schedule` and then `execute`. This method needs to have the machine in which you want to execute the circuit as a mandatory input. If the execution is on an AWS machine, it is needed to specify the S3 bucket too. Also, the provider is only needed when using Quirk URLs.

.. code-block:: python

    from autoscheduler import Autoscheduler

    circuit = "https://algassert.com/quirk#circuit={'cols':[['H'],['•','X'],['Measure','Measure']]}"
    max_qubits = 4
    shots = 100
    provider = 'aws'
    autoscheduler = Autoscheduler()
    results = autoscheduler.schedule_and_execute(circuit, shots, 'ionq', max_qubits=max_qubits, provider=provider, s3_bucket=('amazon-braket-s3' 'my_braket_results'))

.. code-block:: python

    from autoscheduler import Autoscheduler

    circuit = "https://raw.githubusercontent.com/user/repo/branch/file.py"
    max_qubits = 15
    shots = 1000
    autoscheduler = Autoscheduler()
    results = autoscheduler.schedule_and_execute(circuit, shots, 'ibm_brisbane', max_qubits=max_qubits)

.. code-block:: python

    from autoscheduler import Autoscheduler
    from braket.circuits import Circuit

    circuit = Circuit()
    circuit.x(0)
    circuit.cnot(0,1)

    max_qubits = 8
    shots = 300
    autoscheduler = Autoscheduler()
    results = autoscheduler.schedule_and_execute(circuit, shots, 'ionq', max_qubits=max_qubits, s3_bucket=('amazon-braket-s3' 'my_braket_results'))

.. code-block:: python

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

In schedule and schedule and execute you can use the machine to infer the value of max_qubits. It is mandatory to use at least one of those parameters to build the scheduled circuit.

.. code-block:: python

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

.. code-block:: python

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

QCRAFT AutoScheduler will utilize the default AWS and IBM Cloud credentials stored on the machine for cloud executions.