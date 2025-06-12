import unittest
import qiskit
from qiskit.qasm3 import dumps
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

            qreg_q = QuantumRegister(6,'q')
            creg_c = ClassicalRegister(6,'c')
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
            circuit.y(qreg_q[2]).c_if(creg_c[2], 1) # qreg_q[2]
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
                circuit.rx(0, 0.15)
                circuit.ms(0, 1, np.pi/2, np.pi, 0.15)      
                return executeAWS(s3_folder, gate_machines_arn[machine], circuit, shots)

            def execute_quantum_task():
                return random_number_aws('sv1',10)

            print(execute_quantum_task())
            sys.stdout.flush()
            """,
            "ibm_text_if_test":
            """
            from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
            from qiskit import execute, Aer
            from qiskit import transpile
            from qiskit_ibm_provider import least_busy, IBMProvider
            import numpy as np

            qreg_q = QuantumRegister(6,'q')
            creg_c = ClassicalRegister(6,'c')
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
            with circuit.if_test((creg_c[1],1)):
                circuit.x(qreg_q[1]) # qreg_q[1]
                circuit.y(qreg_q[2]) # qreg_q[2]
            with circuit.if_test((creg_c,1)):
                circuit.z(qreg_q[1]) # qreg_q[1]               
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
            "empty_circuit":
            """
            from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
            circuit = QuantumCircuit()"""
        }
        self.scheduler = Autoscheduler()


    def test_code_to_circuit_ibm(self):
        code_str = """
        qreg = QuantumRegister(4, 'reg_qreg')
        creg = ClassicalRegister(4, 'reg_creg')
        circuit = QuantumCircuit(qreg, creg)
        circuit.h(qreg[1+0])
        circuit.cx(qreg[1+0], qreg[0])
        circuit.swap(qreg[1+0         ], qreg[0])
        circuit.cswap(qreg[1+0], qreg[0], qreg[1+1])
        circuit.ccx(qreg[1+0], qreg[0], qreg[1+1])
        circuit.rz(0.1,    qreg[1+0])
        circuit.cu(0.12,0.15,0.2,0.3, qreg[1+1], qreg[0])
        mc_x_gate = MCMT(XGate(), 1, 1)
        circuit.append(mc_x_gate, [qreg[1+0], qreg[0]])
        mc_y_gate = MCMT(YGate(), 2, 1)
        circuit.append(mc_y_gate, [qreg[1+0], qreg[1 + 1] ,qreg[0]])
        mc_z_gate = MCMT(ZGate(), 3, 1)
        circuit.append(mc_z_gate, [qreg[0+0], qreg[  2] ,qreg[1 + 2] ,qreg[ 1 ]])
        circuit.measure(qreg[0], creg[0])
        circuit.measure(qreg[1+0], creg[1])
        circuit.measure(qreg[1  +    1], creg[2          ])
        """
        built_circuit = self.scheduler._code_to_circuit_ibm(code_str)
        self.assertIsInstance(built_circuit, qiskit.QuantumCircuit)
        qreg = qiskit.QuantumRegister(4, 'reg_qreg')
        creg = qiskit.ClassicalRegister(4, 'reg_creg')
        circuit = qiskit.QuantumCircuit(qreg, creg)
        circuit.h(qreg[1+0])
        circuit.cx(qreg[1+0], qreg[0])
        circuit.swap(qreg[1+0         ], qreg[0])
        circuit.cswap(qreg[1+0], qreg[0], qreg[1+1])
        circuit.ccx(qreg[1+0], qreg[0], qreg[1+1])
        circuit.rz(0.1,    qreg[1+0])
        circuit.cu(0.12,0.15,0.2,0.3, qreg[1+1], qreg[0])
        mcx = qiskit.circuit.library.MCXGate(1)
        circuit.append(mcx, [qreg[1+0]] + [qreg[0]])
        circuit.sdg(qreg[0])
        mcx = qiskit.circuit.library.MCXGate(2)
        circuit.append(mcx, [qreg[1+0], qreg[1 + 1]] + [qreg[0]])
        circuit.s(qreg[0])
        circuit.h(qreg[1])
        mcx = qiskit.circuit.library.MCXGate(3)
        circuit.append(mcx, [qreg[0+0], qreg[  2] ,qreg[1 + 2]] + [qreg[1]])
        circuit.h(qreg[1])
        circuit.measure(qreg[0], creg[0])
        circuit.measure(qreg[1+0], creg[1])
        circuit.measure(qreg[1  +    1], creg[2          ])
        # Check if built_circuit is equal to circuit (at gate level)
        built_circuit.remove_final_measurements(inplace=True)
        circuit.remove_final_measurements(inplace=True)
        built_circuit_statevector = qiskit.quantum_info.Statevector.from_instruction(built_circuit)
        circuit_statevector = qiskit.quantum_info.Statevector.from_instruction(circuit)
        self.assertEqual(built_circuit_statevector, circuit_statevector) # As MCX add a label to the gate in qasm and its random, its a better approach to test this with statevectors

    @patch('autoscheduler.Autoscheduler._fetch_circuit')
    def test_code_to_circuit_ibm_with_if_test(self, mock_fetch_circuit):
        mock_response = Mock()
        mock_response.text = self.common_values["ibm_text_if_test"]
        mock_fetch_circuit.return_value = mock_response

        url = "https://raw.githubusercontent.com/example/circuits/main/circuit.py"
        shots = 5000
        max_qubits = 29
        scheduled_circuit, shots, times = self.scheduler.schedule(url, shots, max_qubits=max_qubits, provider='ibm')
        
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
            if self.scheduler._get_qiskit_version() < 2:
                circuit.x(qreg_q[1+6*i]).c_if(creg_c[1+6*i], 1)
                circuit.y(qreg_q[2+6*i]).c_if(creg_c[1+6*i], 1)
                circuit.z(qreg_q[1+6*i]).c_if(creg_c, 1)
            else:
                with circuit.if_test((creg_c[1+6*i],1)):
                    circuit.x(qreg_q[1+6*i])
                    circuit.y(qreg_q[2+6*i])
                with circuit.if_test((creg_c,1)):
                    circuit.z(qreg_q[1+6*i])
            circuit.measure(qreg_q[0+6*i], creg_c[0+6*i])
            circuit.measure(qreg_q[1+6*i], creg_c[1+6*i])
            circuit.measure(qreg_q[2+6*i], creg_c[2+6*i])
            circuit.measure(qreg_q[3+6*i], creg_c[3+6*i])
            circuit.measure(qreg_q[4+6*i], creg_c[4+6*i])
            circuit.measure(qreg_q[5+6*i], creg_c[5+6*i])

        self.assertEqual(dumps(scheduled_circuit), dumps(circuit))
        self.assertEqual(shots, 1250)
        self.assertEqual(times, 4)

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
        scheduled_circuit, shots, times = self.scheduler.schedule(quirk_url, shots, max_qubits=max_qubits, provider=provider)
        
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
        scheduled_circuit, shots, times = self.scheduler.schedule(quirk_url, shots, max_qubits=max_qubits, provider=provider)

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
        scheduled_circuit, shots, times = self.scheduler.schedule(url, shots, max_qubits=max_qubits, provider='ibm')
        
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
        scheduled_circuit, shots, times = self.scheduler.schedule(url, shots, max_qubits=max_qubits, provider='ibm')
        
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
            if self.scheduler._get_qiskit_version() < 2:
                circuit.x(qreg_q[1+6*i]).c_if(creg_c, 1)
                circuit.y(qreg_q[2+6*i]).c_if(creg_c[2+6*i], 1)
            else:
                with circuit.if_test((creg_c, 1)):
                    circuit.x(qreg_q[1+6*i])
                with circuit.if_test((creg_c[2+6*i], 1)):
                    circuit.y(qreg_q[2+6*i])
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
        scheduled_circuit, shots, times = self.scheduler.schedule(url, shots, max_qubits=max_qubits, provider='aws')
        
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
        scheduled_circuit, shots, times = self.scheduler.schedule(url, shots, max_qubits=max_qubits, provider='aws')
        
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
            circuit.rx(0+4*i, 0.15)
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
        scheduled_circuit, shots, times = self.scheduler.schedule(circuit, shots, max_qubits=max_qubits)
    

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
        for i in range(3):  # the measurements are delayed in the autoscheduled circuit
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
        scheduled_circuit, shots, times = self.scheduler.schedule(circuit, shots, max_qubits=max_qubits)

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

    @patch('autoscheduler.Autoscheduler._fetch_circuit')
    def test_schedule_ibm_no_registry_name_github_url(self, mock_fetch_circuit):

        code_str = """
        from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

        qreg = QuantumRegister(3)
        creg = ClassicalRegister(3)
        circuit = QuantumCircuit(qreg, creg)
        circuit.h(qreg[0])
        circuit.cx(qreg[0], qreg[1])
        circuit.measure(qreg[0], creg[0])
        circuit.measure(qreg[1], creg[1])
        """ # No registry name (q or c) on github url

        mock_response = Mock()
        mock_response.text = code_str
        mock_fetch_circuit.return_value = mock_response

        url = "https://raw.githubusercontent.com/example/circuits/main/circuit.py"
        shots = 5000
        max_qubits = 6
        scheduled_circuit, shots1, times = self.scheduler.schedule(url, shots, max_qubits=max_qubits, provider='ibm')
        scheduled_circuit.delay_measure = True

        qreg = qiskit.QuantumRegister(6, 'qreg_q')
        creg = qiskit.ClassicalRegister(6, 'creg_c')
        circuit = qiskit.QuantumCircuit(qreg, creg)
        for i in range(2):
            circuit.h(qreg[0+3*i])
            circuit.cx(qreg[0+3*i], qreg[1+3*i])
            circuit.measure(qreg[0+3*i], creg[0+3*i])
            circuit.measure(qreg[1+3*i], creg[1+3*i])

        self.assertEqual(dumps(scheduled_circuit), dumps(circuit))
        self.assertEqual(shots1, 2500)

    def test_schedule_ibm_no_registry_name_circuit(self):
        shots = 5000
        max_qubits = 6
        qreg = qiskit.QuantumRegister(3) # No q
        creg = qiskit.ClassicalRegister(3) # No c
        circuit = qiskit.QuantumCircuit(qreg, creg) # No registry name on circuit
        circuit.h(qreg[0])
        circuit.cx(qreg[0], qreg[1])
        circuit.measure(qreg[0], creg[0])
        circuit.measure(qreg[1], creg[1])
        scheduled_circuit, shots, times = self.scheduler.schedule(circuit, shots, max_qubits=max_qubits, provider='ibm')

        qreg = qiskit.QuantumRegister(6, 'qreg_q')
        creg = qiskit.ClassicalRegister(6, 'creg_c')
        circuit = qiskit.QuantumCircuit(qreg, creg)
        for i in range(2):
            circuit.h(qreg[0+3*i])
            circuit.cx(qreg[0+3*i], qreg[1+3*i])
        for i in range(2): #delayed measurements
            circuit.measure(qreg[0+3*i], creg[0+3*i])
            circuit.measure(qreg[1+3*i], creg[1+3*i])

        self.assertEqual(dumps(scheduled_circuit), dumps(circuit))
        self.assertEqual(shots, 2500)

    def test_schedule_empty_string(self):
        circuit = ""
        with pytest.raises(TypeError, match="Invalid circuit format. Expected a circuit object, a Quirk URL, or a GitHub URL."):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"])
        with pytest.raises(TypeError, match="Invalid circuit format. Expected a circuit object, a Quirk URL, or a GitHub URL."):
            results = self.scheduler.schedule_and_execute(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"], provider='ibm', machine='local')

    def test_schedule_none_circuit(self):
        circuit = None
        with pytest.raises(TypeError, match="Circuit cannot be None."):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"])
        with pytest.raises(TypeError, match="Circuit cannot be None."):
            results = self.scheduler.schedule_and_execute(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"], machine='local')

    def test_schedule_invalid_quirk_url(self):
        circuit = "https://algassert.com/quirk#circuit={}"
        provider = 'aws'
        with pytest.raises(ValueError, match="Invalid Quirk URL"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"], provider=provider)

    def test_schedule_raw_github_url_without_content(self):
        circuit = "https://raw.githubusercontent.com/"
        with pytest.raises(ValueError, match="Invalid GitHub URL. Expected a URL in the format 'https://raw.githubusercontent.com/user/repo/branch/file'."):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"])
        with pytest.raises(ValueError, match="Invalid GitHub URL. Expected a URL in the format 'https://raw.githubusercontent.com/user/repo/branch/file'."):
            results = self.scheduler.schedule_and_execute(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"], machine='local')            

    def test_schedule_github_url_without_raw(self):
        circuit = "https://github.com/example/repo/"
        with pytest.raises(ValueError, match="URL must come from a raw GitHub file"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"])
        with pytest.raises(ValueError, match="URL must come from a raw GitHub file"):
            results = self.scheduler.schedule_and_execute(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"], machine='local')

    def test_schedule_github_element_without_raw(self):
        circuit = "https://github.com/example/repo/blob/branch/file.py"
        with pytest.raises(ValueError, match="URL must come from a raw GitHub file"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"])
        with pytest.raises(ValueError, match="URL must come from a raw GitHub file"):
            results = self.scheduler.schedule_and_execute(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"], machine='local')


    def test_schedule_github_file_without_raw(self):
        circuit = "https://github.com/example/repo/branch/file.py"
        with pytest.raises(ValueError, match="URL must come from a raw GitHub file"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"])
        with pytest.raises(ValueError, match="URL must come from a raw GitHub file"):
            rseults = self.scheduler.schedule_and_execute(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"], machine='local')

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
        with pytest.raises(ValueError, match='The GitHub URL must be a Braket or Qiskit quantum circuit'):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"])
        with pytest.raises(ValueError, match='The GitHub URL must be a Braket or Qiskit quantum circuit'):
            results = self.scheduler.schedule_and_execute(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"], machine='local')

    def test_schedule_no_qubits_braket_circuit(self):
        circuit = braket.circuits.Circuit()
        with pytest.raises(ValueError, match='The circuit must have at least one qubit and one gate'):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"])
        with pytest.raises(ValueError, match='The circuit must have at least one qubit and one gate'):
            results = self.scheduler.schedule_and_execute(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"], machine='local')            

    def test_schedule_no_qubits_qiskit_circuit(self):
        circuit = qiskit.QuantumCircuit()
        with pytest.raises(ValueError, match='The circuit must have at least one qubit and one gate'):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"])
        with pytest.raises(ValueError, match='The circuit must have at least one qubit and one gate'):
            results = self.scheduler.schedule_and_execute(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"], machine='local')            

    def test_schedule_no_classical_register_qiskit_circuit(self):
        qreg = qiskit.QuantumRegister(2)
        circuit = qiskit.QuantumCircuit(qreg)
        with pytest.raises(ValueError, match='The qiskit circuit must contain a quantum and classical register'):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"])
        with pytest.raises(ValueError, match='The qiskit circuit must contain a quantum and classical register'):
            results = self.scheduler.schedule_and_execute(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"], machine='local')

    def test_schedule_no_quantum_register_qiskit_circuit(self):
        creg = qiskit.ClassicalRegister(2)
        circuit = qiskit.QuantumCircuit(creg)
        with pytest.raises(ValueError, match="The circuit must have at least one qubit and one gate"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"])
        with pytest.raises(ValueError, match="The circuit must have at least one qubit and one gate"):
            results = self.scheduler.schedule_and_execute(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"], machine='local')

    def test_schedule_qiskit_circuit_without_gates(self):
        qreg = qiskit.QuantumRegister(2)
        creg = qiskit.ClassicalRegister(2)
        circuit = qiskit.QuantumCircuit(qreg,creg)
        with pytest.raises(ValueError, match="The circuit must have at least one qubit and one gate"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"])
        with pytest.raises(ValueError, match="The circuit must have at least one qubit and one gate"):
            results = self.scheduler.schedule_and_execute(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"], machine='local')

    def test_schedule_inferior_qubit_number_qiskit(self):
        qreg = qiskit.QuantumRegister(2)
        creg = qiskit.ClassicalRegister(2)
        circuit = qiskit.QuantumCircuit(qreg,creg)
        circuit.h(qreg[0])
        circuit.h(qreg[1])
        max_qubits=1
        with pytest.raises(ValueError, match="Circuit too large"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["shots"], max_qubits=max_qubits)
        with pytest.raises(ValueError, match="Circuit too large"):
            results = self.scheduler.schedule_and_execute(circuit, self.common_values["shots"], max_qubits=max_qubits, machine='local')

    def test_schedule_inferior_qubit_number_braket(self):
        circuit = braket.circuits.Circuit()
        circuit.h(0)
        circuit.h(1)
        max_qubits=1
        with pytest.raises(ValueError, match="Circuit too large"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["shots"], max_qubits=max_qubits)
        with pytest.raises(ValueError, match="Circuit too large"):
            results = self.scheduler.schedule_and_execute(circuit, self.common_values["shots"], max_qubits=max_qubits, machine='local')

    def test_schedule_inferior_qubit_number_quirk(self):
        circuit = "https://algassert.com/quirk#circuit={'cols':[['H'],['•','X'],['Measure','Measure']]}"
        max_qubits=1
        provider = 'ibm'
        with pytest.raises(ValueError, match="Circuit too large"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["shots"], max_qubits=max_qubits, provider=provider)
        with pytest.raises(ValueError, match="Circuit too large"):
            results = self.scheduler.schedule_and_execute(circuit, self.common_values["shots"], max_qubits=max_qubits, provider=provider, machine='local')

    @patch('autoscheduler.Autoscheduler._fetch_circuit')
    def test_schedule_inferior_qubit_number_github_braket(self, mock_fetch_circuit):
        mock_response = Mock()
        mock_response.text = self.common_values["aws_text"]

        mock_fetch_circuit.return_value = mock_response
        circuit = "https://raw.githubusercontent.com/example/circuits/main/circuit.py"
        max_qubits=1
        with pytest.raises(ValueError, match="Circuit too large"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["shots"], max_qubits=max_qubits)
        with pytest.raises(ValueError, match="Circuit too large"):
            results = self.scheduler.schedule_and_execute(circuit, self.common_values["shots"], max_qubits=max_qubits, machine='local')

    @patch('autoscheduler.Autoscheduler._fetch_circuit')
    def test_schedule_inferior_qubit_number_github_qiskit(self, mock_fetch_circuit):
        mock_response = Mock()
        mock_response.text = self.common_values["ibm_text"]

        mock_fetch_circuit.return_value = mock_response
        circuit = "https://raw.githubusercontent.com/example/circuits/main/circuit.py"
        max_qubits=1
        with pytest.raises(ValueError, match="Circuit too large"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["shots"], max_qubits=max_qubits)
        with pytest.raises(ValueError, match="Circuit too large"):
            results = self.scheduler.schedule_and_execute(circuit, self.common_values["shots"], max_qubits=max_qubits, machine='local')

    def test_schedule_quirk_without_provider(self):
        circuit = "https://algassert.com/quirk#circuit={'cols':[['H'],['•','X'],['Measure','Measure']]}"
        with pytest.raises(ValueError, match="Provider not specified"):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"])
        with pytest.raises(ValueError, match="Provider not specified"):
            results = self.scheduler.schedule_and_execute(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"], machine='local')

    def test_schedule_number(self):
        circuit = 2
        with pytest.raises(TypeError, match="Circuit cannot be a number."):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"])
        with pytest.raises(TypeError, match="Circuit cannot be a number."):
            results = self.scheduler.schedule_and_execute(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"], machine='local')

    def test_schedule_iterable_object(self):
        circuit = {}
        with pytest.raises(TypeError, match="Invalid circuit format. Expected a circuit object, a Quirk URL, or a GitHub URL."):
            scheduled_circuit, shots, times = self.scheduler.schedule(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"])
        with pytest.raises(TypeError, match="Invalid circuit format. Expected a circuit object, a Quirk URL, or a GitHub URL."):
            results = self.scheduler.schedule_and_execute(circuit, self.common_values["shots"], max_qubits=self.common_values["max_qubits"], machine='local')
 

    def test_execute_aws_no_bucket(self):
        circuit = braket.circuits.Circuit()
        circuit.h(0)
        with pytest.raises(ValueError, match="S3 Bucket not specified"):
            self.scheduler.execute(circuit, self.common_values["shots"], 'notlocal', 1)
        with pytest.raises(ValueError, match="Machine notlocal not available"):
            self.scheduler.schedule_and_execute(circuit, self.common_values["shots"], 'notlocal')

    def test_no_machine_no_max_qubits(self):
        circuit = braket.circuits.Circuit()
        circuit.h(0)
        with pytest.raises(ValueError, match="Either max_qubits or machine must be specified."):
            self.scheduler.schedule(circuit, self.common_values["shots"])

    def test_max_qubits_over_machine_circuit(self): #Check if using max_qubits will result on not inferring qubits from the machine
        baseCircuit = braket.circuits.Circuit()
        baseCircuit.h(0)

        scheduled_circuit, shots, times = self.scheduler.schedule(baseCircuit, self.common_values["shots"], max_qubits=2, machine='invalid_machine') #It should use the qubits specified on max_qubits

        circuit = braket.circuits.Circuit()
        circuit.h(0)
        circuit.h(1)

        self.assertEqual(scheduled_circuit, circuit)
        self.assertEqual(shots, 50)
        self.assertEqual(times, 2)

    @patch('autoscheduler.Autoscheduler._fetch_circuit')
    def test_max_qubits_over_machine_github_url(self, mock_fetch_circuit): #Check if using max_qubits will result on not inferring qubits from the machine
        mock_response = Mock()
        mock_response.text = self.common_values["ibm_text"]
        mock_fetch_circuit.return_value = mock_response

        url = "https://raw.githubusercontent.com/example/circuits/main/circuit.py"
        shots = 5000
        max_qubits = 29
        scheduled_circuit, shots, times = self.scheduler.schedule(url, shots, max_qubits=max_qubits, machine='invalid_machine') #It should use the qubits specified on max_qubits
        
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

    def test_max_qubits_over_machine_quirk_url(self): #Check if using max_qubits will result on not inferring qubits from the machine
        baseCircuit = "https://algassert.com/quirk#circuit={'cols':[['H'],['Measure']]}"

        scheduled_circuit, shots, times = self.scheduler.schedule(baseCircuit, self.common_values["shots"], max_qubits=2, machine='invalid_machine', provider='aws') #It should use the qubits specified on max_qubits

        circuit = braket.circuits.Circuit()
        circuit.h(0)
        circuit.h(1)

        self.assertEqual(scheduled_circuit, circuit)
        self.assertEqual(shots, 50)
        self.assertEqual(times, 2)

    def test_decompose(self):
        counts = {'00': 2500, '11': 2500} # 2 qubits(2 qubits/2 times, the real circuit has 1 qubit) -> 0:2500 + 0:2500=0:5000. Same for 1
        newcounts = self.scheduler._decompose(counts,5000,2,2,'ibm')
        
        counts2 = {'001101': 500, '110010': 300, '010101':500} # 6 qubits (6 qubits/3 times, the real circuit has 2 qubits) -> 00:500 + 00:300 = 00:800, ... same for the rest values
        newcounts2 = self.scheduler._decompose(counts2,1300,6,3,'ibm')
        
        self.assertEqual(newcounts, {'0': 5000, '1': 5000})
        self.assertEqual(newcounts2, {'00': 800, '11': 800, '01':2000, '10':300})

    def test_get_qubits_not_circuit(self):
        circuit = 'circuit = QuantumCircuit()'
        with pytest.raises(TypeError, match='Invalid circuit type. Expected a Qiskit or Braket circuit.'):
            scheduled_circuit, shots, times = self.scheduler._get_qubits_circuit_object(circuit)

    def test_analyze_circuit_no_gates(self):
        circuit = self.common_values["empty_circuit"]
        with pytest.raises(ValueError, match='The circuit must have at least one qubit and one gate'):
            self.scheduler._analyze_circuit(False, False, circuit)

    def test_compose_aws_no_gates(self):
        circuit = braket.circuits.Circuit()
        with pytest.raises(ValueError, match='The circuit must have at least one qubit and one gate'):
            self.scheduler._compose_circuit(self.common_values['max_qubits'], 5, circuit, self.common_values['shots'], 'aws')

    def test_get_gate_operation(self):
        qreg = qiskit.QuantumRegister(2, 'qreg_q')
        creg = qiskit.ClassicalRegister(2, 'creg_c')
        circuit = qiskit.QuantumCircuit(qreg,creg)
        gate_meas = 'circuit.measure(qreg[0], creg[0])'
        gate_barrier = 'circuit.barrier(qreg)'
        gate_cx = 'circuit.cx(qreg[0], qreg[1])'
        gate_h = 'circuit.h(qreg[0])'
        gate_x = 'circuit.x(qreg[0])'
        gate_y = 'circuit.y(qreg[0])'
        gate_z = 'circuit.z(qreg[0])'
        gate_s = 'circuit.s(qreg[0])'
        gate_t = 'circuit.t(qreg[0])'
        gate_non_existent = 'non_existent_gate'
        gate_non_existent2 = 'circuit.non_existent(qreg[0])'

        result_meas = self.scheduler._get_gate_operation(gate_meas, circuit, qreg, creg)
        result_barrier = self.scheduler._get_gate_operation(gate_barrier, circuit, qreg, creg)
        result_cx = self.scheduler._get_gate_operation(gate_cx, circuit, qreg, creg)
        result_h = self.scheduler._get_gate_operation(gate_h, circuit, qreg, creg)
        result_x = self.scheduler._get_gate_operation(gate_x, circuit, qreg, creg)
        result_y = self.scheduler._get_gate_operation(gate_y, circuit, qreg, creg)
        result_z = self.scheduler._get_gate_operation(gate_z, circuit, qreg, creg)
        result_s = self.scheduler._get_gate_operation(gate_s, circuit, qreg, creg)
        result_t = self.scheduler._get_gate_operation(gate_t, circuit, qreg, creg)
        result_non_existent = self.scheduler._get_gate_operation(gate_non_existent, circuit, qreg, creg)

        with self.assertRaises(AttributeError):
            result_non_existent2 = self.scheduler._get_gate_operation(gate_non_existent2, circuit, qreg, creg)

        self.assertIsInstance(result_meas, qiskit.circuit.instructionset.InstructionSet)
        self.assertEqual(result_meas[0].operation.name, 'measure')

        self.assertIsInstance(result_barrier, qiskit.circuit.instructionset.InstructionSet)
        self.assertEqual(result_barrier[0].operation.name, 'barrier')

        self.assertIsInstance(result_cx, qiskit.circuit.instructionset.InstructionSet)
        self.assertEqual(result_cx[0].operation.name, 'cx')

        self.assertIsInstance(result_h, qiskit.circuit.instructionset.InstructionSet)
        self.assertEqual(result_h[0].operation.name, 'h')

        self.assertIsInstance(result_x, qiskit.circuit.instructionset.InstructionSet)
        self.assertEqual(result_x[0].operation.name, 'x')

        self.assertIsInstance(result_y, qiskit.circuit.instructionset.InstructionSet)
        self.assertEqual(result_y[0].operation.name, 'y')

        self.assertIsInstance(result_z, qiskit.circuit.instructionset.InstructionSet)
        self.assertEqual(result_z[0].operation.name, 'z')

        self.assertIsInstance(result_s, qiskit.circuit.instructionset.InstructionSet)
        self.assertEqual(result_s[0].operation.name, 's')

        self.assertIsInstance(result_t, qiskit.circuit.instructionset.InstructionSet)
        self.assertEqual(result_t[0].operation.name, 't')

        self.assertIsNone(result_non_existent)
        
    def test_qiskit_version(self):
        version = self.scheduler._get_qiskit_version()
        self.assertIsInstance(version, int)
        self.assertGreaterEqual(version, 0)

        with patch('importlib.metadata.version') as mock_version:
            mock_version.return_value = "1.2.3"
            result = self.scheduler._get_qiskit_version()
            self.assertEqual(result, 1)

            mock_version.return_value = "2.0.1"
            result = self.scheduler._get_qiskit_version()
            self.assertEqual(result, 2)

            mock_version.return_value = "0.45.2"
            result = self.scheduler._get_qiskit_version()
            self.assertEqual(result, 0)

            mock_version.return_value = "3.1.0rc1"
            result = self.scheduler._get_qiskit_version()
            self.assertEqual(result, 3)

            mock_version.return_value = "2.5.0.dev0+abc123" #Dev version
            result = self.scheduler._get_qiskit_version()
            self.assertEqual(result, 2)

            mock_version.return_value = "v2.1.0" #Starting with string
            result = self.scheduler._get_qiskit_version()
            self.assertEqual(result, 1)

            mock_version.return_value = "5" #Failed regex
            result = self.scheduler._get_qiskit_version()
            self.assertEqual(result, 1)

if __name__ == '__main__':
    unittest.main()