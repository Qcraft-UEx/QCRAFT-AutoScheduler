import unittest
import qiskit
from qiskit.qasm2 import dumps
import braket.circuits
import pytest
from unittest.mock import Mock, patch
from autoscheduler import Autoscheduler
import numpy as np

class TestAutoScheduler(unittest.TestCase):
    def setUp(self):
        self.common_values = {
            "max_qubits": 10,
            "shots": 100,
            "ibm_text":
            """
            from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
            from qiskit import execute, Aer
            from qiskit import transpile
            from qiskit_ibm_provider import least_busy, IBMProvider
            import numpy as np

            qreg_q = QuantumRegister(6, 'q')
            creg_c = ClassicalRegister(6, 'c')
            circuit = QuantumCircuit(qreg_q, creg_c)
            gate_machines_arn= {"local":"local", "ibm_brisbane":"ibm_brisbane", "ibm_osaka":"ibm_osaka", "ibm_kyoto":"ibm_kyoto", "simulator_stabilizer":"simulator_stabilizer", "simulator_mps":"simulator_mps", "simulator_extended_stabilizer":"simulator_extended_stabilizer", "simulator_statevector":"simulator_statevector"}

            circuit.h(qreg_q[0])
            circuit.h(qreg_q[1])
            circuit.h(qreg_q[2])
            circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2], qreg_q[3], qreg_q[4], qreg_q[5])
            circuit.cx(qreg_q[0], qreg_q[3])
            circuit.cx(qreg_q[1], qreg_q[4])
            circuit.cx(qreg_q[2], qreg_q[5])
            circuit.cx(qreg_q[1], qreg_q[4])
            circuit.cx(qreg_q[1], qreg_q[5])
            circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2], qreg_q[3], qreg_q[4], qreg_q[5])
            circuit.h(qreg_q[0])
            circuit.h(qreg_q[1])
            circuit.h(qreg_q[2])
            circuit.measure(qreg_q[0], creg_c[0])
            circuit.measure(qreg_q[1], creg_c[1])
            circuit.measure(qreg_q[2], creg_c[2])
            circuit.measure(qreg_q[3], creg_c[3])
            circuit.measure(qreg_q[4], creg_c[4])
            circuit.measure(qreg_q[5], creg_c[5])

            shots = 10000
            provider = IBMProvider()
            backend = Aer.get_backend('qasm_simulator')

            qc_basis = transpile(circuit, backend)
            job = execute(qc_basis, backend=backend, shots=shots)
            job_result = job.result()
            print(job_result.get_counts(qc_basis))
            """,

            "aws_text":
            """
            import sys
            from braket.circuits import Gate
            from braket.circuits import Circuit
            from braket.devices import LocalSimulator
            from braket.aws import AwsDevice

            def executeAWS(s3_folder, machine, circuit, shots):
                if machine=="local":
                    device = LocalSimulator()
                    result = device.run(circuit, int(shots)).result()
                    counts = result.measurement_counts
                    return counts

                device = AwsDevice(machine)

                if "sv1" not in machine and "tn1" not in machine:
                    task = device.run(circuit, s3_folder, int(shots), poll_timeout_seconds=5 * 24 * 60 * 60)
                else:
                    task = device.run(circuit, s3_folder, int(shots))
                return 'finished'

            def random_number_aws(machine, shots):  # noqa: E501
                gate_machines_arn= { "riggeti_aspen8":"arn:aws:braket:::device/qpu/rigetti/Aspen-8", "riggeti_aspen9":"arn:aws:braket:::device/qpu/rigetti/Aspen-9", "riggeti_aspen11":"arn:aws:braket:::device/qpu/rigetti/Aspen-11", "riggeti_aspen_m1":"arn:aws:braket:us-west-1::device/qpu/rigetti/Aspen-M-1", "DM1":"arn:aws:braket:::device/quantum-simulator/amazon/dm1","oqc_lucy":"arn:aws:braket:eu-west-2::device/qpu/oqc/Lucy", "borealis":"arn:aws:braket:us-east-1::device/qpu/xanadu/Borealis", "ionq":"arn:aws:braket:::device/qpu/ionq/ionQdevice", "sv1":"arn:aws:braket:::device/quantum-simulator/amazon/sv1", "tn1":"arn:aws:braket:::device/quantum-simulator/amazon/tn1", "local":"local"}
                ######
                #RELLENAR S3_FOLDER_ID#
                ######
                s3_folder = ('amazon-braket-s3, 'api') #bucket name, folder name
                ######
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
                circuit.cnot(3,0)             
                return executeAWS(s3_folder, gate_machines_arn[machine], circuit, shots)

            def execute_quantum_task():
                return random_number_aws('sv1',10)

            print(execute_quantum_task())
            sys.stdout.flush()
            """,
            "ibm_text_errors":
            """
            from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
            from qiskit import execute, Aer
            from qiskit import transpile
            from qiskit_ibm_provider import least_busy, IBMProvider
            import numpy as np

            qreg_q = QuantumRegister(6, 'q')
            creg_c = ClassicalRegister(6, 'c')
            circuit = QuantumCircuit(qreg_q, creg_c)
            gate_machines_arn= {"local":"local", "ibm_brisbane":"ibm_brisbane", "ibm_osaka":"ibm_osaka", "ibm_kyoto":"ibm_kyoto", "simulator_stabilizer":"simulator_stabilizer", "simulator_mps":"simulator_mps", "simulator_extended_stabilizer":"simulator_extended_stabilizer", "simulator_statevector":"simulator_statevector"}

            circuit.h(qreg_q[0])              
            circuit.h(qreg_q[1])   
            circuit.h(qreg_q[2]) 
            circuit.barrier(qreg_q[  0 ],qreg_q[ 1  ], qreg_q[2], qreg_q[3], qreg_q[4], qreg_q[5])
            circuit.cx(qreg_q[0],qreg_q[3]) 
            circuit.cx(qreg_q[  1  ], qreg_q[4])      # np.pi    
            circuit.cx(qreg_q[2  ], qreg_q[  5])
            circuit.barrier() #circuit.barrier(qreg_q)
            circuit.cx(qreg_q[1], qreg_q[ 4])  #changing creg_c[3]   
            circuit.cx(qreg_q[1], qreg_q[5 ])  
            circuit.barrier(qreg_q[0],qreg_q[1],qreg_q[2], qreg_q[3],qreg_q[4], qreg_q[5]) # editing qreg_q 
            circuit.h(qreg_q[0]) #qreg_q[1]
            circuit.h(qreg_q[1]) # changing the qreg_q[1] creg_c[2] 
            circuit.h(qreg_q[2]) # 
            circuit.rx(np.pi / 4 , qreg_q[ 0 ]) #creg_c
            circuit.barrier(qreg_q) #circuit.barrier(qreg_q)
            #circuit.rx(np.pi / 4 , qreg_q[ 0 ]) #creg_c
            circuit.x(qreg_q[1]).c_if(creg_c, 1) # qreg_q[1]
            circuit.measure(qreg_q[0],creg_c[0])   #qreg_c[1
            circuit.measure(qreg_q[1], creg_c[1])  #121]
            circuit.measure(qreg_q[2], creg_c[2])  # sa1
            circuit.measure(qreg_q[3], creg_c[3]) # circuit.h(qreg_q[2])
            circuit.measure(qreg_q[4], creg_c[4])
            circuit.measure(qreg_q[5], creg_c[5])

            shots = 10000
            provider = IBMProvider()
            backend = Aer.get_backend('qasm_simulator')

            qc_basis = transpile(circuit, backend)
            job = execute(qc_basis, backend=backend, shots=shots)
            job_result = job.result()
            print(job_result.get_counts(qc_basis))
            """,
            "aws_text_errors":
            """
            import sys
            from braket.circuits import Gate
            from braket.circuits import Circuit
            from braket.devices import LocalSimulator
            from braket.aws import AwsDevice

            def executeAWS(s3_folder, machine, circuit, shots):
                if machine=="local":
                    device = LocalSimulator()
                    result = device.run(circuit, int(shots)).result()
                    counts = result.measurement_counts
                    return counts

                device = AwsDevice(machine)

                if "sv1" not in machine and "tn1" not in machine:
                    task = device.run(circuit, s3_folder, int(shots), poll_timeout_seconds=5 * 24 * 60 * 60)
                else:
                    task = device.run(circuit, s3_folder, int(shots))
                return 'finished'

            def random_number_aws(machine, shots):  # noqa: E501
                gate_machines_arn= { "riggeti_aspen8":"arn:aws:braket:::device/qpu/rigetti/Aspen-8", "riggeti_aspen9":"arn:aws:braket:::device/qpu/rigetti/Aspen-9", "riggeti_aspen11":"arn:aws:braket:::device/qpu/rigetti/Aspen-11", "riggeti_aspen_m1":"arn:aws:braket:us-west-1::device/qpu/rigetti/Aspen-M-1", "DM1":"arn:aws:braket:::device/quantum-simulator/amazon/dm1","oqc_lucy":"arn:aws:braket:eu-west-2::device/qpu/oqc/Lucy", "borealis":"arn:aws:braket:us-east-1::device/qpu/xanadu/Borealis", "ionq":"arn:aws:braket:::device/qpu/ionq/ionQdevice", "sv1":"arn:aws:braket:::device/quantum-simulator/amazon/sv1", "tn1":"arn:aws:braket:::device/quantum-simulator/amazon/tn1", "local":"local"}
                ######
                #RELLENAR S3_FOLDER_ID#
                ######
                s3_folder = ('amazon-braket-s3, 'api') #bucket name, folder name
                ######
                circuit = Circuit()
                circuit.x(0  )
                circuit.x(  1)    
                circuit.x(2)
                circuit.x( 3 )      
                circuit.cnot(2, 1) # chaning qubit 1
                circuit.cnot( 1 ,2) #
                circuit.cnot(2,1)  # 121
                circuit.cnot(1,0) # 4
                circuit.cnot( 0,1) # qub1
                circuit.cnot(1,0)   # ]sada
                circuit.cnot( 3  ,0) #np 
                circuit.cnot(0,3)   # np.pi
                circuit.cnot(3 ,0)  # circuit.cnot(1)
                circuit.cphaseshift10(0, 1, np.pi )           
                circuit.gpi2(0, np.pi/4)
                circuit.ms(0, 1, np.pi/2, np.pi, 0.15)      
                return executeAWS(s3_folder, gate_machines_arn[machine], circuit, shots)

            def execute_quantum_task():
                return random_number_aws('sv1',10)

            print(execute_quantum_task())
            sys.stdout.flush()
            """,
        }
        self.scheduler = Autoscheduler()


    def test_code_to_circuit_ibm(self):
        code_str = """
        qreg = QuantumRegister(3, 'reg_qreg')
        creg = ClassicalRegister(3, 'reg_creg')
        circuit = QuantumCircuit(qreg, creg)
        circuit.h(qreg[1+0])
        circuit.cx(qreg[1+0], qreg[0])
        circuit.swap(qreg[1+0         ], qreg[0])
        circuit.cswap(qreg[1+0], qreg[0], qreg[1+1])
        circuit.ccx(qreg[1+0], qreg[0], qreg[1+1])
        circuit.rz(0.1,    qreg[1+0])
        circuit.cu(0.12,0.15,0.2,0.3, qreg[1+1], qreg[0])
        circuit.measure(qreg[0], creg[0])
        circuit.measure(qreg[1+0], creg[1])
        circuit.measure(qreg[1  +    1], creg[2          ])
        """
        built_circuit = self.scheduler._code_to_circuit_ibm(code_str)
        self.assertIsInstance(built_circuit, qiskit.QuantumCircuit)
        qreg = qiskit.QuantumRegister(3, 'reg_qreg')
        creg = qiskit.ClassicalRegister(3, 'reg_creg')
        circuit = qiskit.QuantumCircuit(qreg, creg)
        circuit.h(qreg[1+0])
        circuit.cx(qreg[1+0], qreg[0])
        circuit.swap(qreg[1+0         ], qreg[0])
        circuit.cswap(qreg[1+0], qreg[0], qreg[1+1])
        circuit.ccx(qreg[1+0], qreg[0], qreg[1+1])
        circuit.rz(0.1,    qreg[1+0])
        circuit.cu(0.12,0.15,0.2,0.3, qreg[1+1], qreg[0])
        circuit.measure(qreg[0], creg[0])
        circuit.measure(qreg[1+0], creg[1])
        circuit.measure(qreg[1  +    1], creg[2          ])
        # Check if built_circuit is equal to circuit (at gate level)
        self.assertEqual(dumps(built_circuit), dumps(circuit))

    def test_code_to_circuit_aws(self):
        code_str = """circuit.x(0)\ncircuit.x(0+  1)\ncircuit.x(     2)\ncircuit.x(3)\ncircuit.cnot(2,1)\ncircuit.cnot(1,2)\ncircuit.cnot(   1+1   ,1)\ncircuit.cnot(1,0)\ncircuit.cnot(0,     1    )\ncircuit.cnot(1,0)\ncircuit.cnot(3,0)\ncircuit.cnot(0,3)\ncircuit.ccnot(3,0,1)\ncircuit.rx(1,0)\ncircuit.cswap(0, 1, 2)\ncircuit.phaseshift(0,0.15)\ncircuit.cphaseshift01( 0, 1,     0.15)\ncircuit.s(2)\ncircuit.gpi2(0, 0.15)\ncircuit.yy(0, 1, 0.15)\ncircuit.ms(0, 1, 0.15, 0.15, 0.15)
        """
        
        built_circuit = self.scheduler._code_to_circuit_aws(code_str)
        self.assertIsInstance(built_circuit, braket.circuits.Circuit)

        circuit = braket.circuits.Circuit()
        circuit.x(0)
        circuit.x(0+  1)
        circuit.x(     2)
        circuit.x(3)
        circuit.cnot(2,1)
        circuit.cnot(1,2)
        circuit.cnot(   1+1   ,1)
        circuit.cnot(1,0)
        circuit.cnot(0,     1    )
        circuit.cnot(1,0)
        circuit.cnot(3,0)
        circuit.cnot(0,3)
        circuit.ccnot(3,0,1)
        circuit.rx(1,0)
        circuit.cswap(0, 1, 2)
        circuit.phaseshift(0,0.15)
        circuit.cphaseshift01( 0, 1,     0.15)
        circuit.s(2)
        circuit.gpi2(0, 0.15)
        circuit.yy(0, 1, 0.15)
        circuit.ms(0, 1, 0.15, 0.15, 0.15)
        # Check if built_circuit is equal to circuit (at gate level)
        self.assertEqual(built_circuit, circuit)

    def test_schedule_quirk_ibm(self):
        quirk_url = "https://algassert.com/quirk#circuit={'cols':[['H'],['•','X'],['Measure','Measure']]}"
        shots = 5000
        machine = "local"
        max_qubits = 4
        provider = 'ibm'
        scheduled_circuit, shots, times = self.scheduler.schedule(quirk_url, max_qubits, shots, provider)
        
        qreg = qiskit.QuantumRegister(4, 'qreg_q')
        creg = qiskit.ClassicalRegister(4, 'creg_c')
        circuit = qiskit.QuantumCircuit(qreg, creg)
        circuit.h(qreg[0])
        circuit.cx(qreg[0], qreg[1])
        circuit.measure(qreg[0], creg[0])
        circuit.measure(qreg[1], creg[1])
        circuit.h(qreg[2])
        circuit.cx(qreg[2], qreg[3])
        circuit.measure(qreg[2], creg[2])
        circuit.measure(qreg[3], creg[3])

        self.assertEqual(dumps(scheduled_circuit), dumps(circuit))
        self.assertEqual(shots, 2500)
        self.assertEqual(times, 2)


    def test_schedule_quirk_aws(self):
        quirk_url = "https://algassert.com/quirk#circuit={'cols':[['H'],['•','X'],['Measure','Measure']]}"
        shots = 5000
        machine = "local"
        max_qubits = 4
        provider = 'aws'
        scheduled_circuit, shots, times = self.scheduler.schedule(quirk_url, max_qubits, shots, provider)

        circuit = braket.circuits.Circuit()
        circuit.h(0)
        circuit.cnot(0, 1)
        circuit.h(2)
        circuit.cnot(2, 3)

        self.assertEqual(scheduled_circuit, circuit)
        self.assertEqual(shots, 2500)
        self.assertEqual(times, 2)

    @patch('autoscheduler.Autoscheduler._fetch_circuit')
    def test_schedule_github_url_ibm(self, mock_fetch_circuit):

        mock_response = Mock()
        mock_response.text = self.common_values["ibm_text"]
        mock_fetch_circuit.return_value = mock_response

        url = "https://raw.githubusercontent.com/example/circuits/main/circuit.py"
        shots = 5000
        max_qubits = 29
        scheduled_circuit, shots, times = self.scheduler.schedule(url, max_qubits, shots, provider='ibm')
        
        qreg_q = qiskit.QuantumRegister(24, 'qreg_q')
        creg_c = qiskit.ClassicalRegister(24, 'creg_c')
        circuit = qiskit.QuantumCircuit(qreg_q, creg_c)
        for i in range(4):
            circuit.h(qreg_q[0+6*i])
            circuit.h(qreg_q[1+6*i])
            circuit.h(qreg_q[2+6*i])
            circuit.barrier(qreg_q[0+6*i], qreg_q[1+6*i], qreg_q[2+6*i], qreg_q[3+6*i], qreg_q[4+6*i], qreg_q[5+6*i])
            circuit.cx(qreg_q[0+6*i], qreg_q[3+6*i])
            circuit.cx(qreg_q[1+6*i], qreg_q[4+6*i])
            circuit.cx(qreg_q[2+6*i], qreg_q[5+6*i])
            circuit.cx(qreg_q[1+6*i], qreg_q[4+6*i])
            circuit.cx(qreg_q[1+6*i], qreg_q[5+6*i])
            circuit.barrier(qreg_q[0+6*i], qreg_q[1+6*i], qreg_q[2+6*i], qreg_q[3+6*i], qreg_q[4+6*i], qreg_q[5+6*i])
            circuit.h(qreg_q[0+6*i])
            circuit.h(qreg_q[1+6*i])
            circuit.h(qreg_q[2+6*i])
            circuit.measure(qreg_q[0+6*i], creg_c[0+6*i])
            circuit.measure(qreg_q[1+6*i], creg_c[1+6*i])
            circuit.measure(qreg_q[2+6*i], creg_c[2+6*i])
            circuit.measure(qreg_q[3+6*i], creg_c[3+6*i])
            circuit.measure(qreg_q[4+6*i], creg_c[4+6*i])
            circuit.measure(qreg_q[5+6*i], creg_c[5+6*i])
        
        self.assertEqual(dumps(scheduled_circuit), dumps(circuit))
        self.assertEqual(shots, 1250)
        self.assertEqual(times, 4)

    @patch('autoscheduler.Autoscheduler._fetch_circuit')
    def test_schedule_github_url_ibm_with_errors(self, mock_fetch_circuit):

        mock_response = Mock()
        mock_response.text = self.common_values["ibm_text_errors"]
        mock_fetch_circuit.return_value = mock_response

        url = "https://raw.githubusercontent.com/example/circuits/main/circuit.py"
        shots = 5000
        max_qubits = 29
        scheduled_circuit, shots, times = self.scheduler.schedule(url, max_qubits, shots, provider='ibm')
        
        qreg_q = qiskit.QuantumRegister(24, 'qreg_q')
        creg_c = qiskit.ClassicalRegister(24, 'creg_c')
        circuit = qiskit.QuantumCircuit(qreg_q, creg_c)
        for i in range(4):
            circuit.h(qreg_q[0+6*i])
            circuit.h(qreg_q[1+6*i])
            circuit.h(qreg_q[2+6*i])
            circuit.barrier(qreg_q[0+6*i], qreg_q[1+6*i], qreg_q[2+6*i], qreg_q[3+6*i], qreg_q[4+6*i], qreg_q[5+6*i])
            circuit.cx(qreg_q[0+6*i], qreg_q[3+6*i])
            circuit.cx(qreg_q[1+6*i], qreg_q[4+6*i])
            circuit.cx(qreg_q[2+6*i], qreg_q[5+6*i])
            circuit.barrier()
            circuit.cx(qreg_q[1+6*i], qreg_q[4+6*i])
            circuit.cx(qreg_q[1+6*i], qreg_q[5+6*i])
            circuit.barrier(qreg_q[0+6*i], qreg_q[1+6*i], qreg_q[2+6*i], qreg_q[3+6*i], qreg_q[4+6*i], qreg_q[5+6*i])
            circuit.h(qreg_q[0+6*i])
            circuit.h(qreg_q[1+6*i])
            circuit.h(qreg_q[2+6*i])
            circuit.rx(np.pi / 4 , qreg_q[ 0+6*i])
            circuit.barrier(qreg_q)
            circuit.x(qreg_q[1+6*i]).c_if(creg_c, 1)
            circuit.measure(qreg_q[0+6*i], creg_c[0+6*i])
            circuit.measure(qreg_q[1+6*i], creg_c[1+6*i])
            circuit.measure(qreg_q[2+6*i], creg_c[2+6*i])
            circuit.measure(qreg_q[3+6*i], creg_c[3+6*i])
            circuit.measure(qreg_q[4+6*i], creg_c[4+6*i])
            circuit.measure(qreg_q[5+6*i], creg_c[5+6*i])

        self.assertEqual(dumps(scheduled_circuit), dumps(circuit))
        self.assertEqual(shots, 1250)
        self.assertEqual(times, 4)

    @patch('autoscheduler.Autoscheduler._fetch_circuit')
    def test_schedule_github_url_aws(self, mock_fetch_circuit):
        mock_response = Mock()
        mock_response.text = self.common_values["aws_text"]
        
        mock_fetch_circuit.return_value = mock_response

        url = "https://raw.githubusercontent.com/example/circuits/main/circuit.py"
        shots = 5000
        max_qubits = 16
        scheduled_circuit, shots, times = self.scheduler.schedule(url, max_qubits, shots, provider='aws')
        
        circuit = braket.circuits.Circuit()
        for i in range(4):
            circuit.x(0+4*i)
            circuit.x(1+4*i)
            circuit.x(2+4*i)
            circuit.x(3+4*i)   
            circuit.cnot(2+4*i,1+4*i)
            circuit.cnot(1+4*i,2+4*i)
            circuit.cnot(2+4*i,1+4*i)
            circuit.cnot(1+4*i,0+4*i)
            circuit.cnot(0+4*i,1+4*i)
            circuit.cnot(1+4*i,0+4*i)
            circuit.cnot(3+4*i,0+4*i)
            circuit.cnot(0+4*i,3+4*i)
            circuit.cnot(3+4*i,0+4*i)

        self.assertEqual(scheduled_circuit, circuit)
        self.assertEqual(shots, 1250)
        self.assertEqual(times, 4)

    @patch('autoscheduler.Autoscheduler._fetch_circuit')
    def test_schedule_github_url_aws_with_errors(self, mock_fetch_circuit):
        mock_response = Mock()
        mock_response.text = self.common_values["aws_text_errors"]
        
        mock_fetch_circuit.return_value = mock_response

        url = "https://raw.githubusercontent.com/example/circuits/main/circuit.py"
        shots = 5000
        max_qubits = 16
        scheduled_circuit, shots, times = self.scheduler.schedule(url, max_qubits, shots, provider='aws')
        
        circuit = braket.circuits.Circuit()
        for i in range(4):
            circuit.x(0+4*i)
            circuit.x(1+4*i)
            circuit.x(2+4*i)
            circuit.x(3+4*i)   
            circuit.cnot(2+4*i,1+4*i)
            circuit.cnot(1+4*i,2+4*i)
            circuit.cnot(2+4*i,1+4*i)
            circuit.cnot(1+4*i,0+4*i)
            circuit.cnot(0+4*i,1+4*i)
            circuit.cnot(1+4*i,0+4*i)
            circuit.cnot(3+4*i,0+4*i)
            circuit.cnot(0+4*i,3+4*i)
            circuit.cnot(3+4*i,0+4*i)
            circuit.cphaseshift10(0+4*i, 1+4*i, np.pi)
            circuit.gpi2(0+4*i, np.pi/4)
            circuit.ms(0+4*i, 1+4*i, np.pi/2, np.pi, 0.15)

        self.assertEqual(scheduled_circuit, circuit)
        self.assertEqual(shots, 1250)
        self.assertEqual(times, 4)

    def test_schedule_circuit_ibm(self):

        qreg = qiskit.QuantumRegister(3, 'qreg_q')
        creg = qiskit.ClassicalRegister(3, 'creg_c')
        circuit = qiskit.QuantumCircuit(qreg, creg)
        circuit.h(qreg[1])
        circuit.cx(qreg[1], qreg[0])
        circuit.swap(qreg[1], qreg[0])
        circuit.cswap(qreg[1], qreg[0], qreg[2])
        circuit.ccx(qreg[1], qreg[0], qreg[2])
        circuit.rz(0.1,    qreg[1])
        circuit.cu(0.12,np.pi,0.2,0.3, qreg[2], qreg[0])
        circuit.measure(qreg[0], creg[0])
        circuit.measure(qreg[1], creg[1])
        circuit.measure(qreg[2], creg[2])

        shots = 5000
        machine = "local"
        max_qubits = 9
        scheduled_circuit, shots, times = self.scheduler.schedule(circuit, max_qubits, shots)
    

        qreg = qiskit.QuantumRegister(9, 'qreg_q')
        creg = qiskit.ClassicalRegister(9, 'creg_c')
        new_circuit = qiskit.QuantumCircuit(qreg, creg)
        for i in range(3):
            new_circuit.h(qreg[1+i*3])
            new_circuit.cx(qreg[1+i*3], qreg[0+i*3])
            new_circuit.swap(qreg[1+i*3], qreg[0+i*3])
            new_circuit.cswap(qreg[1+i*3], qreg[0+i*3], qreg[2+i*3])
            new_circuit.ccx(qreg[1+i*3], qreg[0+i*3], qreg[2+i*3])
            new_circuit.rz(0.1,    qreg[1+i*3])
            new_circuit.cu(0.12,np.pi,0.2,0.3, qreg[2+i*3], qreg[0+i*3])
            new_circuit.measure(qreg[0+i*3], creg[0+i*3])
            new_circuit.measure(qreg[1+i*3], creg[1+i*3])
            new_circuit.measure(qreg[2+i*3], creg[2+i*3])



        self.assertEqual(dumps(scheduled_circuit), dumps(new_circuit))
        self.assertEqual(shots, 1667)
        self.assertEqual(times, 3)

    def test_schedule_circuit_aws(self):


        circuit = braket.circuits.Circuit()
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
        circuit.rx( 1 , 0)
        circuit.cswap(0, 1, 2)
        circuit.phaseshift(0 , 0.15)
        circuit.cphaseshift10(0, 1, 0.15)
        circuit.s([1, 2])
        circuit.gpi2(0, 0.15)
        circuit.yy(0, 1, 0.15)
        circuit.ms(0, 1, np.pi/2, 0.15, 0.15)

        shots = 5000
        machine = "local"
        max_qubits = 16
        scheduled_circuit, shots, times = self.scheduler.schedule(circuit, max_qubits, shots)

        new_circuit = braket.circuits.Circuit()
        for i in range(4):
            new_circuit.x(0+i*4)
            new_circuit.x(1+i*4)
            new_circuit.x(2+i*4)
            new_circuit.x(3+i*4)   
            new_circuit.cnot(2+i*4,1+i*4)
            new_circuit.cnot(1+i*4,2+i*4)
            new_circuit.cnot(2+i*4,1+i*4)
            new_circuit.cnot(1+i*4,0+i*4)
            new_circuit.cnot(0+i*4,1+i*4)
            new_circuit.cnot(1+i*4,0+i*4)
            new_circuit.cnot(3+i*4,0+i*4)
            new_circuit.cnot(0+i*4,3+i*4)
            new_circuit.ccnot(3+i*4,0+i*4,1+i*4)  
            new_circuit.rx(1+i*4,0)
            new_circuit.cswap(0+i*4, 1+i*4, 2+i*4)
            new_circuit.phaseshift(0+i*4,0.15)
            new_circuit.cphaseshift10(0+i*4, 1+i*4, 0.15)
            new_circuit.s([1+i*4, 2+i*4])
            new_circuit.gpi2(0+i*4, 0.15)
            new_circuit.yy(0+i*4, 1+i*4, 0.15)
            new_circuit.ms(0+i*4, 1+i*4, np.pi/2, 0.15, 0.15)

        self.assertEqual(scheduled_circuit, new_circuit)
        self.assertEqual(shots, 1250)
        self.assertEqual(times, 4)

    def test_schedule_empty_string(self):
        circuit = ""
        with pytest.raises(TypeError, match="Invalid circuit format. Expected a circuit object, a Quirk URL, or a GitHub URL."):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["max_qubits"], self.common_values["shots"])

    def test_schedule_none_circuit(self):
        circuit = None
        with pytest.raises(TypeError, match="Circuit cannot be None."):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["max_qubits"], self.common_values["shots"])

    def test_schedule_invalid_quirk_url(self):
        circuit = "https://algassert.com/quirk#circuit={}"
        provider = 'aws'
        with pytest.raises(ValueError, match="Invalid Quirk URL"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["max_qubits"], self.common_values["shots"], provider)

    def test_schedule_raw_github_url_without_content(self):
        circuit = "https://raw.githubusercontent.com/"
        with pytest.raises(ValueError, match="Invalid GitHub URL. Expected a URL in the format 'https://raw.githubusercontent.com/user/repo/branch/file'."):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["max_qubits"], self.common_values["shots"])

    def test_schedule_github_url_without_raw(self):
        circuit = "https://github.com/example/repo/"
        with pytest.raises(ValueError, match="URL must come from a raw GitHub file"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["max_qubits"], self.common_values["shots"])

    def test_schedule_github_element_without_raw(self):
        circuit = "https://github.com/example/repo/blob/branch/file.py"
        with pytest.raises(ValueError, match="URL must come from a raw GitHub file"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["max_qubits"], self.common_values["shots"])

    def test_schedule_github_file_without_raw(self):
        circuit = "https://github.com/example/repo/branch/file.py"
        with pytest.raises(ValueError, match="URL must come from a raw GitHub file"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["max_qubits"], self.common_values["shots"])

    @patch('autoscheduler.Autoscheduler._fetch_circuit')
    def test_schedule_raw_github_url_without_circuit(self, mock_fetch_circuit):
        mock_response = Mock()
        mock_response.text = """
        circuits:
          - name: circuit1
            gates:
              - type: H
                target: 0
          - name: circuit2
            gates:
              - type: X
                target: 1
        """
        mock_fetch_circuit.return_value = mock_response
        circuit = "https://raw.githubusercontent.com/user/repo/branch/file.yaml"
        with pytest.raises(ValueError, match="The GitHub URL must be a Braket or Qiskit quantum circuit"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["max_qubits"], self.common_values["shots"])

    def test_schedule_no_qubits_braket_circuit(self):
        circuit = braket.circuits.Circuit()
        with pytest.raises(ValueError, match="The circuit must have at least one qubit and one gate"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["max_qubits"], self.common_values["shots"])

    def test_schedule_no_qubits_qiskit_circuit(self):
        circuit = qiskit.QuantumCircuit()
        with pytest.raises(ValueError, match="The qiskit circuit must contain a quantum and classical register"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["max_qubits"], self.common_values["shots"])

    def test_schedule_no_classical_register_qiskit_circuit(self):
        qreg = qiskit.QuantumRegister(2)
        circuit = qiskit.QuantumCircuit(qreg)
        with pytest.raises(ValueError, match="The qiskit circuit must contain a quantum and classical register"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["max_qubits"], self.common_values["shots"])

    def test_schedule_no_quantum_register_qiskit_circuit(self):
        creg = qiskit.ClassicalRegister(2)
        circuit = qiskit.QuantumCircuit(creg)
        with pytest.raises(ValueError, match="The qiskit circuit must contain a quantum and classical register"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["max_qubits"], self.common_values["shots"])
        
    def test_schedule_qiskit_circuit_without_gates(self):
        qreg = qiskit.QuantumRegister(2)
        creg = qiskit.ClassicalRegister(2)
        circuit = qiskit.QuantumCircuit(qreg,creg)
        with pytest.raises(ValueError, match="The circuit must have at least one qubit and one gate"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["max_qubits"], self.common_values["shots"])

    def test_schedule_inferior_qubit_number_qiskit(self):
        qreg = qiskit.QuantumRegister(2)
        creg = qiskit.ClassicalRegister(2)
        circuit = qiskit.QuantumCircuit(qreg,creg)
        circuit.h(qreg[0])
        circuit.h(qreg[1])
        max_qubits=1
        with pytest.raises(ValueError, match="Circuit too large"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, max_qubits, self.common_values["shots"])

    def test_schedule_inferior_qubit_number_braket(self):
        circuit = braket.circuits.Circuit()
        circuit.h(0)
        circuit.h(1)
        max_qubits=1
        with pytest.raises(ValueError, match="Circuit too large"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, max_qubits, self.common_values["shots"])

    def test_schedule_inferior_qubit_number_quirk(self):
        circuit = "https://algassert.com/quirk#circuit={'cols':[['H'],['•','X'],['Measure','Measure']]}"
        max_qubits=1
        provider = 'ibm'
        with pytest.raises(ValueError, match="Circuit too large"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, max_qubits, self.common_values["shots"],provider)

    @patch('autoscheduler.Autoscheduler._fetch_circuit')
    def test_schedule_inferior_qubit_number_github_braket(self, mock_fetch_circuit):
        mock_response = Mock()
        mock_response.text = self.common_values["aws_text"]

        mock_fetch_circuit.return_value = mock_response
        circuit = "https://raw.githubusercontent.com/example/circuits/main/circuit.py"
        max_qubits=1
        with pytest.raises(ValueError, match="Circuit too large"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, max_qubits, self.common_values["shots"])

    @patch('autoscheduler.Autoscheduler._fetch_circuit')
    def test_schedule_inferior_qubit_number_github_qiskit(self, mock_fetch_circuit):
        mock_response = Mock()
        mock_response.text = self.common_values["ibm_text"]

        mock_fetch_circuit.return_value = mock_response
        circuit = "https://raw.githubusercontent.com/example/circuits/main/circuit.py"
        max_qubits=1
        with pytest.raises(ValueError, match="Circuit too large"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, max_qubits, self.common_values["shots"])

    def test_schedule_quirk_without_provider(self):
        circuit = "https://algassert.com/quirk#circuit={'cols':[['H'],['•','X'],['Measure','Measure']]}"
        with pytest.raises(ValueError, match="Provider not specified"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["max_qubits"], self.common_values["shots"])

    def test_schedule_number(self):
        circuit = 2
        with pytest.raises(TypeError, match="Circuit cannot be a number."):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["max_qubits"], self.common_values["shots"])

    def test_schedule_iterable_object(self):
        circuit = {}
        with pytest.raises(TypeError, match="Invalid circuit format. Expected a circuit object, a Quirk URL, or a GitHub URL."):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["max_qubits"], self.common_values["shots"])

if __name__ == '__main__':
    unittest.main()