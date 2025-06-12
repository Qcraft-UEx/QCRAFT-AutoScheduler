"""
Module containing the Autoscheduler class
"""
from typing import Union, Tuple, Optional
import re
import math
import ast
from urllib.parse import unquote, urlparse
import numpy as np
import requests
import qiskit
import braket
from braket.circuits import Circuit
from ._executeCircuitIBM import _runIBM, _get_qubits_machine_ibm
from ._executeCircuitAWS import _runAWS, _get_qubits_machine_aws
from ._divideResults import _divideResults
from ._translator import _get_ibm_individual, _get_aws_individual


class Autoscheduler:
    """
    A class used to compose quantum circuits with themselves, obtaining a new circuit with a higher number of qubits but less number of shots needed.
    
    The supported quantum circuit types are Qiskit and Braket. It can also work with GitHub raw URLs containing a circuit or Quirk URLs.
    """
    def __init__(self):
        """
        Initializes a new instance of the Autoscheduler class, capable of composing quantum circuits with themselves to reduce the number of shots needed to execute them.
        The circuit can be a Qiskit circuit, a Braket circuit, a GitHub raw URL with a circuit, or a Quirk URL.

        The new instance will prepare the Autoscheduler to work with the available circuit types.
        """
        self._available_circuit_types = {'braket':braket.circuits.Circuit, 'qiskit':qiskit.QuantumCircuit} #A dictionary mapping the names of circuit types ('braket' and 'qiskit') to their corresponding classes.

    def schedule(self, circuit: Union[qiskit.QuantumCircuit, Circuit, str], shots:int, machine: Optional[str] = None, max_qubits:Optional[int] = None, provider: Optional[str] = None) -> Tuple[Union[qiskit.QuantumCircuit, Circuit], int, int]:
         # Compose the circuit, it can be a circuit, github url of a circuit or quirk url of a circuit
        """
        Composes the circuit multiple time to reduce the number of shots needed to execute the circuit.

        Args:
            circuit (qiskit.QuantumCircuit | braket.circuits.Circuit | str): The circuit that will be scheduled, it can be a Qiskit circuit, Braket circuit, GitHub raw URL with a circuit or a Quirk URL.
            shots (int): The initial number of shots that the composed circuit will be executed.
            max_qubits (int, optional): The maximum number of qubits that the composed circuit can have. If None, `machine` must be specified to infer it.            
            machine (str, optional): The machine that will execute the circuit. It can be 'local' or the name of the machine on 'ibm' or 'aws'. For 'aws' it can be either the name or the ARN of the machine. If None, `max_qubits` must be specified.            
            provider (str, optional): The provider of the circuit. It can be 'ibm', 'aws' or None. If None, it will be inferred from the circuit, it is only mandatory when Quirk URL is used.

        Returns:
            tuple: A 3-tuple containing the composed circuit (qiskit.QuantumCircuit or braket.circuits.Circuit), the new and reduced number of shots for the scheduled circuit (int), and the number of times the circuit was composed to reduce the number of shots (int).

        Raises:
            ValueError: If the `circuit` is too large; if the `provider` is not specified using a Quirk URL; if the `machine` is not specified when `max_qubits` is None; or if the `machine` is not None and is not available on the IBM or AWS account.
            TypeError: If the `circuit` is None, a number, or in an invalid format.
        """
        if circuit is None:
            raise TypeError("Circuit cannot be None.")
        if isinstance(circuit, (int, float)):
            raise TypeError("Circuit cannot be a number.")
        if max_qubits is None and machine is None:
            raise ValueError("Either max_qubits or machine must be specified.")
        if not isinstance(circuit, str) and any(isinstance(circuit, ctype) for ctype in self._available_circuit_types.values()): #Circuit object
            circuit, qubits, provider = self._get_qubits_circuit_object(circuit) #Get the string circuit of the cicuit, also the qubits and the provider to check if its fits within the max_qubits
            max_qubits = self._get_qubits_machine(machine, provider) if max_qubits is None else max_qubits
            if max_qubits < qubits:
                raise ValueError("Circuit too large")
            circ,shots,times = self._compose_circuit(max_qubits, qubits, circuit, shots, provider)  # Based on the circuit, it composes itself multiple times
        elif 'algassert' in circuit:
            if provider is None:
                raise ValueError("Provider not specified")
            qubits = self._get_qubits_url(circuit) #Analyzes the quirk url that includes the circuit to get the qubits it has to check if it fits within the max_qubits
            max_qubits = self._get_qubits_machine(machine, provider) if max_qubits is None else max_qubits
            if max_qubits < qubits:
                raise ValueError("Circuit too large")
            composed_circuit,shots,times = self._create_circuit_url(max_qubits, qubits, circuit, shots, provider) #Based on the quirk url, it uses the translator to transform it into a string with the gates
            circ = self._get_composed_circuit(composed_circuit, provider)
        elif 'github' in circuit:
            circuit, qubits, provider = self._get_qubits_circuit(circuit) #Gets the content of the github raw file to retrieve the circuit, it parses it and transforms it into a normalized circuit, also gets the qubit number to check if it fits within the max_qubits
            max_qubits = self._get_qubits_machine(machine, provider) if max_qubits is None else max_qubits
            if max_qubits < qubits:
                raise ValueError("Circuit too large")
            composed_circuit,shots,times = self._create_circuit_circuit(max_qubits, qubits, circuit, shots, provider) # Creates the composed circuit
            circ = self._get_composed_circuit(composed_circuit, provider)
        else:
            raise TypeError("Invalid circuit format. Expected a circuit object, a Quirk URL, or a GitHub URL.")

        return circ, shots, times


    def execute(self, circuit: Union[qiskit.QuantumCircuit, Circuit], shots: int, machine: str, times: int, s3_bucket: Optional[tuple] = None) -> dict: # Executes the circuit
        """
        Executes a scheduled circuit and transform the results in the same format as the original circuit.

        Args:
            circuit (qiskit.QuantumCircuit | braket.circuits.Circuit): The circuit that will be executed, it can be a Qiskit circuit, Braket circuit.            
            shots (int): The number of shots that the composed circuit will be executed.            
            machine (str): The machine that will execute the circuit. It can be 'local' or the name of the machine on 'ibm' or 'aws'. For 'aws' it can be either the name or the ARN of the machine.            
            times (int): The number of times that the circuit was composed.
            s3_bucket (tuple, optional): The S3 bucket where the results will be stored. It is only mandatory when `machine` is not 'local' and the circuit will be executed on aws. The format is ('bucket-name', 'folder-name').

        Returns:
            dict: The results of the execution of the composed circuit, taking into account the shots provided.

        Raises: 
            ValueError: If the `s3_bucket` is not specified on a AWS execution in the cloud; or if the `machine` is not available on the IBM or AWS account.
            TypeError: If the `circuit` is None or an invalid format.
        """
        if isinstance(circuit, qiskit.circuit.quantumcircuit.QuantumCircuit):
            provider = 'ibm'
            qubits = circuit.num_qubits
        elif isinstance(circuit, braket.circuits.circuit.Circuit):
            provider = 'aws'
            qubits = circuit.qubit_count
        else:
            raise TypeError("Invalid circuit format. Expected a circuit object.")

        if provider == 'aws' and s3_bucket is None and machine != 'local':
            raise ValueError("S3 Bucket not specified")
        if provider == "ibm":
            counts = _runIBM(machine,circuit,shots)
        elif provider == "aws":
            counts = _runAWS(machine,circuit,shots,s3_bucket)
        return self._decompose(counts,shots,qubits,times, provider)


    def schedule_and_execute(self, circuit:Union[qiskit.QuantumCircuit, Circuit, str], shots:int, machine:str, max_qubits:Optional[int] = None, provider:Optional[str] = None, s3_bucket:Optional[tuple] = None) -> dict: # Compose the circuit
        """
        Composes the circuit multiple time to reduce the number of shots needed to execute the circuit and also executes it.

        Args:
            circuit (qiskit.QuantumCircuit | braket.circuits.Circuit | str): The circuit that will be scheduled and later executed, it can be a Qiskit circuit, Braket circuit, GitHub raw URL with a circuit or a Quirk URL.
            shots (int): The initial number of shots that the composed circuit will be executed.
            machine (str): The machine that will execute the circuit. It can be 'local' or the name of the machine on 'ibm' or 'aws'. For 'aws' it can be either the name or the ARN of the machine.
            max_qubits (int, optional): The maximum number of qubits that the composed circuit can have. If None, the qubits will be inferred from `machine`.
            provider (str, optional): The provider of the circuit. It can be 'ibm', 'aws' or None. If None, it will be inferred from the circuit, it it only mandatory when Quirk URL is used.
            s3_bucket (tuple, optional): The S3 bucket where the results will be stored. It is only mandatory when `machine` is not 'local' and the circuit will be executed on aws. The format is ('bucket-name', 'folder-name').

        Returns:
            dict: The results of the execution of the composed circuit, taking into account the shots provided.

        Raises: 
            ValueError: If the `circuit` is too large; if the `provider` is not specified using a Quirk URL; or if the `machine` is not available on the IBM or AWS account.
            TypeError: If the `circuit` is None, a number, or an invalid format.
        """
        if circuit is None:
            raise TypeError("Circuit cannot be None.")
        if isinstance(circuit, (int, float)):
            raise TypeError("Circuit cannot be a number.")
        if not isinstance(circuit, str) and any(isinstance(circuit, ctype) for ctype in self._available_circuit_types.values()): #Circuit object
            circuit, qubits, provider = self._get_qubits_circuit_object(circuit) #Get the string circuit of the cicuit, also the qubits and the provider to check if its fits within the max_qubits
            max_qubits = self._get_qubits_machine(machine, provider) if max_qubits is None else max_qubits
            if max_qubits < qubits:
                raise ValueError("Circuit too large")
            composed_circuit,shots,times = self._compose_circuit(max_qubits, qubits, circuit, shots, provider)  # Based on the circuit, it composes itself multiple times
        elif 'algassert' in circuit:
            if provider is None:
                raise ValueError("Provider not specified")
            qubits = self._get_qubits_url(circuit) #Analyzes the quirk url that includes the circuit to get the qubits it has to check if it fits within the max_qubits
            max_qubits = self._get_qubits_machine(machine, provider) if max_qubits is None else max_qubits
            if max_qubits < qubits:
                raise ValueError("Circuit too large")
            composed_circuit_str,shots,times = self._create_circuit_url(max_qubits, qubits, circuit, shots, provider) #Based on the quirk url, it uses the translator to transform it into a string with the gates
            composed_circuit = self._get_composed_circuit(composed_circuit_str, provider)
        elif 'github' in circuit:
            circuit, qubits, provider = self._get_qubits_circuit(circuit) #Gets the content of the github raw file to retrieve the circuit, it parses it and transforms it into a normalized circuit, also gets the qubit number to check if it fits within the max_qubits
            max_qubits = self._get_qubits_machine(machine, provider) if max_qubits is None else max_qubits
            if max_qubits < qubits:
                raise ValueError("Circuit too large")
            composed_circuit_str,shots,times = self._create_circuit_circuit(max_qubits, qubits, circuit, shots, provider) # Creates the composed circuit
            composed_circuit = self._get_composed_circuit(composed_circuit_str, provider)
        else:
            raise TypeError("Invalid circuit format. Expected a circuit object, a Quirk URL, or a GitHub URL.")

        results = self.execute(composed_circuit, shots, machine, times, s3_bucket)
        return results


    def _get_qubits_url(self, circuit:str) -> int: # Gets the qubits from a circuit based on its quirk url
        """
        Obtains the number of qubits of a Quirk circuit.

        Args:
            circuit str(Quirk URL): The circuit that will be analyzed.
        
        Returns:
            int: The number of qubits of the circuit.

        Raises: 
            ValueError: If the Quirk URL is invalid.
        """
        fragment = urlparse(circuit).fragment
        try:
            circuit_str = fragment[len('circuit='):]
            circuit = ast.literal_eval(unquote(circuit_str))
            qubits = max(len(col) for col in circuit['cols'] if 1 not in col)
        except Exception as e:
            raise ValueError("Invalid Quirk URL") from e
        return qubits

    def _create_circuit_url(self, max_qubits:int, qubits:int, circuit:str, shots:int, provider:str)-> Tuple[str,int,int]: # Creates the composed circuit based on a quirk url
        """
        Creates a string with the composed circuit based on a Quirk URL.

        Args:
            max_qubits (int): The maximum number of qubits that the composed circuit can have.
            qubits (int): The number of qubits of the circuit.
            circuit (str): The circuit that will be composed.
            shots (int): The initial number of shots that the composed circuit will be executed.
            provider (str): The provider of the circuit. It can be 'ibm', 'aws'.
        
        Returns:
            tuple: A 3-tuple containing the composed circuit (str), the new and reduced number of shots for the scheduled circuit (int), and the number of times the circuit was composed to reduce the number of shots (int).
        """
        #Checks the times it can compose itself
        times =  max_qubits // qubits
        shots = math.ceil(shots / times)
        #For each time it can be composed itself, it translates the quirk url but putting the new qubit numbers
        qc = ""
        if provider == "ibm":
            for i in range(times):
                qc += _get_ibm_individual(circuit,(i*qubits)) + '\n'
            qc = (
                "from numpy import pi\n"
                "import numpy as np\n"
                "from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit\n"
                f"qreg_q = QuantumRegister({qubits*(times)}, 'q')\n"
                f"creg_c = ClassicalRegister({qubits*(times)}, 'c')\n"
                "circuit = QuantumCircuit(qreg_q, creg_c)\n"
                + qc
            )
        elif provider == "aws":
            for i in range(times):
                qc += _get_aws_individual(circuit,(i*qubits)) + '\n'
            qc = (
                "from numpy import pi\n"
                "import numpy as np\n"
                "from collections import Counter\n"
                "from braket.circuits import Circuit\n"
                "circuit = Circuit()\n"
                + qc
            )

        return qc, shots, times

    def _get_qubits_circuit(self, circuit:str) -> Tuple[str,int,str]: # Gets the qubits from a circuit based on its github url
        """
        Obtains the number of qubits of a circuit from a GitHub URL, it also changes the original circuit to be make it standard.

        Args:
            circuit (str): The GitHub URL containing the circuit that will be analyzed.
        
        Returns:
            tuple: A 3-tuple containing the composed circuit (str), the number of qubits of the circuit (int), and the provider of the circuit, that can be either 'ibm' or 'aws' (str).

        Raises: 
            ValueError: If the GitHub URL does not contain a Braket or Qiskit quantum circuit.
        """
        #First, it gets the circuit from the github url
        response = self._fetch_circuit(circuit)

        circuit = response.text
        lines = circuit.split('\n')
        importAWS = next((line for line in lines if 'braket.circuits' in line), None)
        importIBM = next((line for line in lines if 'qiskit' in line), None)

        if importAWS is None and importIBM is None:
            raise ValueError('The GitHub URL must be a Braket or Qiskit quantum circuit')

        circuit, num_qubits = self._analyze_circuit(importIBM, importAWS, lines) # Circuit normalization to get circuit, qr, cr, etc to work better with the circuit string
        provider = 'ibm' if importIBM else 'aws' if importAWS else None
        return circuit, num_qubits, provider

    def _get_qubits_circuit_object(self, circuit: Union[qiskit.QuantumCircuit, Circuit]) -> Tuple[Union[qiskit.QuantumCircuit, Circuit],int,str]: # Get qubits from a circuit object (first it transforms it into a circuit string and reads the number of qubits)
        """
        Obtains the number of qubits of a circuit, it also changes the original circuit to be make it a string.

        Args:
            circuit (qiskit.QuantumCircuit | braket.circuits.Circuit): The circuit that will be analyzed.
        
        Returns:
            tuple: A 3-tuple containing the composed circuit (qiskit.QuantumCircuit | braket.circuits.Circuit), the number of qubits of the circuit (int), and the provider of the circuit, that can be either 'ibm' or 'aws' (str).

        Raises:
            TypeError: If the circuit is not a Qiskit or Braket circuit.
        """
        importAWS, importIBM = False, False
        #Checks the provider to create the circuit string based on that. The circuit string is created becase is needed to create the composed circuit easily by looping and adding the gates again but changing the qubit number
        if isinstance(circuit, qiskit.circuit.quantumcircuit.QuantumCircuit):
            importIBM = True
            num_qubits = circuit.num_qubits
            #circuit = self._circuit_to_code_ibm(circuit)
        elif isinstance(circuit, braket.circuits.circuit.Circuit):
            importAWS = True
            num_qubits = circuit.qubit_count
            #circuit = self._circuit_to_code_aws(circuit)
        else:
            raise TypeError("Invalid circuit type. Expected a Qiskit or Braket circuit.")

        #lines = circuit.split('\n')
        # Check if in lines there is a QuantumCircuit or a Circuit

        #qc, num_qubits = self._analyze_circuit(importIBM, importAWS, lines) #Gets the number of qubits of the circuit and also puts it in a easy way to handle it, naming it into a specific way (circuit, qr, cr...)

        provider = 'ibm' if importIBM else 'aws' if importAWS else None

        return circuit, num_qubits, provider

    def _circuit_to_code_ibm(self, circuit: qiskit.QuantumCircuit) -> str: #This function transforms the ibm circuit to the original code in a string
        """
        Parses the ibm circuit into a string

        Args:
            circuit (qiskit.QuantumCircuit): The circuit that will be parsed.
        
        Returns:
            str: A string representation of the circuit.

        Raises: 
            ValueError: If the circuit does not contain a quantum and classical register.
        """
        code = ""
        try:
            qreg_name = next(iter(circuit.qregs)).name
            creg_name = next(iter(circuit.cregs)).name
        except Exception as e:
            raise ValueError('The qiskit circuit must contain a quantum and classical register') from e


        code += f"{qreg_name} = QuantumRegister({circuit.num_qubits}, '{qreg_name}')\n"
        code += f"{creg_name} = ClassicalRegister({circuit.num_clbits}, '{creg_name}')\n"
        code += f"circuit = QuantumCircuit({qreg_name}, {creg_name})\n"

        for instruction in circuit.data:
            gate = instruction.operation
            qubits = instruction.qubits
            cbits = instruction.clbits
            gate_name = gate.name
            qubit_indices = ', '.join(f"{qreg_name}[{i}]" for i in [circuit.qubits.index(qubit) for qubit in qubits])
            if gate_name == "measure":
                cbit_indices = ', '.join(f"{creg_name}[{i}]" for i in [circuit.clbits.index(cbit) for cbit in cbits])
                code += f"circuit.{gate_name}({qubit_indices}, {cbit_indices})\n"
            elif gate.params:
                params = ', '.join(str(param) for param in gate.params)
                code += f"circuit.{gate_name}({params}, {qubit_indices})\n"
            else:
                code += f"circuit.{gate_name}({qubit_indices})\n"

        return code

    def _circuit_to_code_aws(self, circuit: Circuit)->str: # To get the aws circuit object and transforming to a string
        """
        Parses the aws circuit into a string.

        Args:
            circuit (braket.circuits.Circuit): The circuit that will be parsed.
        
        Returns:
            str: A string representation of the circuit.
        """
        code = "from braket.circuits import Circuit, gates\n\n"
        code += "circuit = Circuit()\n"

        for instr in circuit.instructions:
            gate_name = instr.operator.name
            target_qubits = ', '.join(str(int(qubit)) for qubit in instr.target)

            if gate_name.lower() in ['rx', 'ry', 'rz', 'xx', 'yy', 'zz', 'gpi', 'gpi2'] or 'phaseshift' in gate_name.lower():
                # These gates have a parameter
                param = instr.operator.angle
                code += f"circuit.{gate_name.lower()}({target_qubits},{param})\n"
            elif gate_name.lower() in ['ms']:
                # These gates have 3 parameters
                params_str = str(instr.operator).split("'angles': ")[1].split(", 'qubit_count'")[0]
                params = ', '.join(params_str.strip("()").split(", "))
                code += f"circuit.{gate_name.lower()}({target_qubits},{params})\n"
            else:
                code += f"circuit.{gate_name.lower()}({target_qubits})\n"
        return code

    def _analyze_circuit(self, importIBM:bool, importAWS:bool, lines:list) -> Tuple[str,int]: # Analyzes the circuit string and transforms it to a normalized object to work better with it (changing the name of the circuit, the registries...) also it returns the number of qubits of the circuit
        """
        Analyzes and transforms a string that contains a circuit to make it easier to work with it.

        Args:
            importIBM (bool): True if the circuit is from IBM, False otherwise.
            importAWS (bool): True if the circuit is from AWS, False otherwise.
            lines (list): The lines of the circuit.
        
        Returns:
            tuple: A 2-tuple containing the normalized circuit string (str) and the number of qubits of the circuit (int).

        Raises: 
            ValueError: If the circuit does not contain a qubit and a gate; or if the input is not a quantum circuit.
        """
        qc = None
        num_qubits = 0
        if importIBM:
            num_qubits_line = next((line.split('#')[0].strip() for line in lines if '= QuantumRegister(' in line.split('#')[0]), None)
            num_qubits = int(num_qubits_line.split('QuantumRegister(')[1].split(',')[0].strip(')')) if num_qubits_line else None

            # Get the data before the = in the line that appears QuantumCircuit(...)
            file_circuit_name_line = next((line.split('#')[0].strip() for line in lines if '= QuantumCircuit(' in line.split('#')[0]), None)
            file_circuit_name = file_circuit_name_line.split('=')[0].strip() if file_circuit_name_line else None

            # Get the name of the quantum register
            qreg_line = next((line.split('#')[0].strip() for line in lines if '= QuantumRegister(' in line.split('#')[0]), None)
            qreg = qreg_line.split('=')[0].strip() if qreg_line else None
            # Get the name of the classical register
            creg_line = next((line.split('#')[0].strip() for line in lines if '= ClassicalRegister(' in line.split('#')[0]), None)
            creg = creg_line.split('=')[0].strip() if creg_line else None

            # Remove all lines that don't start with file_circuit_name and don't include the line that has file_circuit_name.add_register and line not starts with // or # (comments)
            circuit_lines = []
            for line in lines:
                clean_line = line.split('#')[0].strip()
                original_line = line.split('#')[0]  # Keep original spacing

                if (clean_line.startswith(file_circuit_name+'.') and 'add_register' not in clean_line) or \
                   clean_line.startswith('with circuit.if_test(') or \
                   original_line.lstrip().startswith('circuit.'):  # Indented circuit operations
                    circuit_lines.append(original_line.rstrip())  # Keep indentation but remove trailing spaces

            circuit = '\n'.join(circuit_lines)


            # Replace all appearances of file_circuit_name, qreg, and creg
            circuit = circuit.replace(file_circuit_name+'.', 'circuit.')
            circuit = circuit.replace(f'{qreg}[', 'qreg_q[')
            circuit = circuit.replace(f'{creg}[', 'creg_c[')

            # Create an array with the same length as the number of qubits initialized to 0 to count the number of gates on each qubit
            qubits = [0] * num_qubits
            for line in circuit.split('\n'): # For each line in the circuit
                if 'measure' not in line and 'barrier' not in line: #If the line is not a measure or a barrier
                    # Check the numbers after qreg_q and add 1 to qubits on that position. It should work with whings like circuit.cx(qreg_q[0], qreg_q[3]), adding 1 to both 0 and 3
                    # This adds 1 to the number of gates used on that qubit
                    for match in re.finditer(r'qreg_q\[(\d+)\]', line):
                        qubits[int(match.group(1))] += 1

            qc = circuit

        elif importAWS:
            file_circuit_name_line = next((line.split('#')[0].strip() for line in lines if '= Circuit(' in line.split('#')[0]), None)
            file_circuit_name = file_circuit_name_line.split('=')[0].strip() if file_circuit_name_line else None

            # Remove all lines that don't start with file_circuit_name and don't include the line that has file_circuit_name.add_register and line not starts with // or # (comments)
            circuit_lines = [line.split('#')[0].strip() for line in lines if line.split('#')[0].strip().startswith(file_circuit_name+'.') and 'add_register' not in line]
            circuit = '\n'.join(circuit_lines)

            circuit = circuit.replace(file_circuit_name+'.', 'circuit.')
            # Remove tabs and spaces at the beginning of the lines
            circuit = '\n'.join([line.lstrip() for line in circuit.split('\n')])

            # Create an array with the same length as the number of qubits initialized to 0 to count the number of gates on each qubit
            qubits = {}
            for line in circuit.split('\n'): # For each line in the circuit
                if 'barrier' not in line and 'circuit.' in line: #If the line is not a measure or a barrier
                    #Get the gate_name, which is the thing after circuit. and before (
                    gate_name = re.search(r'circuit\.(.*?)\(', line).group(1)
                    if gate_name in ['rx', 'ry', 'rz', 'gpi', 'gpi2', 'phaseshift']: # Because different gates have different number of parameters and in braket circuits there is no visual difference between a qubit and a parameter
                        # These gates have a parameter
                        numbers_retrieved = re.findall(r'\d+', line)
                        numbers = numbers_retrieved[0] if numbers_retrieved else None

                    elif gate_name in ['xx', 'yy', 'zz', 'ms'] or 'cphase' in gate_name:
                        # These gates have 2 or more parameters
                        numbers_retrieved = re.findall(r'\d+', line)
                        numbers = numbers[:2] if numbers_retrieved else None

                    else:
                        # These gates have no parameters
                        numbers = re.findall(r'\d+', line)

                    for elem in numbers:
                        if elem not in qubits:
                            qubits[elem] = 0
                        else:
                            qubits[elem] += 1
            num_qubits = len(qubits.values())

            qc = circuit

        if num_qubits == 0 or qubits == [] or max(qubits) == 0:
            raise ValueError('The circuit must have at least one qubit and one gate')
        if qc is None:
            raise ValueError('The input is not a quantum circuit')
        return qc, num_qubits

    def _compose_circuit(self, max_qubits:int, qubits:int, circuit:Union[qiskit.QuantumCircuit, Circuit], shots:int, provider:str) -> Tuple[Union[qiskit.QuantumCircuit, Circuit],int,int]:
        """
        Composes a quantum circuit based on a an object multiple times.

        Args:
            max_qubits (int): The maximum number of qubits that the composed circuit can have.
            qubits (int): The number of qubits of the circuit.            
            circuit (Union[qiskit.QuantumCircuit, braket.circuits.Circuit]): The circuit that will be composed.            
            shots (int): The initial number of shots that the composed circuit will be executed.            
            provider (str): The provider of the circuit. It can be 'ibm', 'aws'.
        
        Returns:
            tuple: A 3-tuple containing the composed circuit (Union[qiskit.QuantumCircuit, braket.circuits.Circuit]), the new and reduced number of shots for the scheduled circuit (int), and the number of times the circuit was composed to reduce the number of shots (int).

        Raises:
            ValueError: If the qiskit circuit does not contain a quantum and classical register.
            ValueError: If the circuit does not contain a qubit and a gate.
        """
        if qubits == 0:
            raise ValueError('The circuit must have at least one qubit and one gate')

        times =  max_qubits // qubits
        shots = math.ceil(shots / times)
        if provider == "ibm":

            if len(circuit.qregs) == 0 or len(circuit.cregs) == 0:
                raise ValueError('The qiskit circuit must contain a quantum and classical register')

            if len(circuit.data) == 0:
                raise ValueError('The circuit must have at least one qubit and one gate')

            circuit_part = circuit.to_instruction(label='original_circuit')

            qreg = qiskit.QuantumRegister(times*qubits, 'qreg_q')
            creg = qiskit.ClassicalRegister(times*qubits, 'creg_c')
            qc = qiskit.QuantumCircuit(qreg, creg)

            for i in range(times):
                qc.append(circuit_part, qreg[i*qubits:qubits + i*qubits], creg[i*qubits:qubits + i*qubits])

            qc = qc.decompose()

        if provider == "aws":

            circuit_part = circuit

            if len(circuit.instructions) == 0:
                raise ValueError('The circuit must have at least one qubit and one gate')

            qc = braket.circuits.Circuit()

            for i in range(times):
                qc.add_circuit(circuit=circuit_part, target=[i*qubits + j for j in range(qubits)])

        return qc, shots, times


    def _create_circuit_circuit(self, max_qubits:int, qubits:int, circuit:str, shots:int, provider:str) -> Tuple[str,int,int]: # Create the composed circuit
        """
        Composes a quantum circuit based on a string multiple times.

        Args:
            max_qubits (int): The maximum number of qubits that the composed circuit can have.
            qubits (int): The number of qubits of the circuit.            
            circuit (str): The circuit that will be composed.            
            shots (int): The initial number of shots that the composed circuit will be executed.            
            provider (str): The provider of the circuit. It can be 'ibm', 'aws'.
        
        Returns:
            tuple: A 3-tuple containing the composed circuit (str), the new and reduced number of shots for the scheduled circuit (int), and the number of times the circuit was composed to reduce the number of shots (int).
        """
        # First, check how many times it can be composed based on the shots
        times =  max_qubits // qubits
        shots = math.ceil(shots / times)

        # It composes itself, adding the base circuit and the same base circuit with changing the qubits
        qc = circuit
        for i in range(times-1):
            edited_circuit = circuit
            # In the circuit, change all [...] to [...+(i*qubits)]
            if provider == "ibm":
                edited_circuit = re.sub(r'\[\s*(\d+)\s*\]', r'[ \g<1>+' + f'{(i+1)*qubits} ]', edited_circuit)
            elif provider == "aws":
                # Get the gate name (circuit. ...)
                new_edited_circuit = ""
                lines = edited_circuit.split('\n')
                for line in lines:
                    gate_name = re.search(r'circuit\.(.*?)\(', line).group(1)

                    if gate_name in ['rx', 'ry', 'rz', 'gpi', 'gpi2', 'phaseshift']:
                        # These gates have a parameter
                        # Edit the first parameter
                        new_edited_circuit += re.sub(rf'{gate_name}\(\s*(\d+)', lambda m: f"{gate_name}({int(m.group(1)) + (i+1)*qubits}", line, count=1) +'\n'
                    elif gate_name in ['xx', 'yy', 'zz','ms'] or 'cphase' in gate_name:
                        # These gates have 2 parameters
                        # Edit the first and second parameters
                        new_edited_circuit += re.sub(rf'{gate_name}\((\d+),\s*(\d+)', lambda m: f"{gate_name}({int(m.group(1)) + (i+1)*qubits},{int(m.group(2)) + (i+1)*qubits}", line, count=1)+'\n'

                    else:
                        # These gates have no parameters, so change the number of qubits on all
                        new_edited_circuit += re.sub(r'(\d+)', lambda m: str(int(m.group(1)) + (i+1)*qubits), line)+'\n'

                edited_circuit = new_edited_circuit

            qc += '\n' + edited_circuit  # Add newline before appending

        # Adds the needed dependencies to it can be converted to a true circuit object after
        if provider == "ibm":
            qc = (
                "from numpy import pi\n"
                "import numpy as np\n"
                "from qiskit.circuit.library import MCXGate, MCMT\n"
                "from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit\n"
                f"qreg_q = QuantumRegister({qubits*(times)}, 'q')\n"
                f"creg_c = ClassicalRegister({qubits*(times)}, 'c')\n"
                "circuit = QuantumCircuit(qreg_q, creg_c)\n"
                + qc
            )
        elif provider == "aws":
            qc = (
                "from numpy import pi\n"
                "import numpy as np\n"
                "from collections import Counter\n"
                "from braket.circuits import Circuit\n"
                "circuit = Circuit()\n"
                + qc
            )

        return qc, shots, times

    def _decompose(self, counts:dict, shots:int, qubits:int, times:int, provider:str) -> dict: # Decompose the composed result
        """
        Decomposes the result to make it like it has been executed the same number of times as the initial number of shots.

        Args:
            counts (dict): The results of the execution of the composed circuit.            
            shots (int): The number of shots that the circuit has been executed.            
            qubits (int): The number of qubits of the circuit.            
            times (int): The number of times that the circuit was composed.            
            provider (str): The provider of the circuit. It can be 'ibm', 'aws'.
        
        Returns:
            dict: The decomposed results of the execution of the composed circuit, taking into account the shots provided.
        """
        qubits_per_composition = int(qubits / times)
        users = [0] * times
        circuit_name = [0] * times
        shots = [shots] * times
        qubits = [qubits_per_composition] * times
        results = _divideResults(counts, shots, provider, qubits, users, circuit_name)
        circuit_results = {}

        for result in results:
            for key, value in result[(0, 0)].items():
                if key not in circuit_results:
                    circuit_results[key] = value
                else:
                    circuit_results[key] += value

        return circuit_results

    def _get_composed_circuit(self, circuit:str, provider:str) -> Union[qiskit.QuantumCircuit, Circuit]: # Get the composed circuit object
        """
        Transforms a string representation of a circuit into a Qiskit or Braket circuit.

        Args:
            circuit (str): The string representation of the circuit.            
            provider (str): The provider of the circuit. It can be 'ibm', 'aws'.
        
        Returns:
            qiskit.QuantumCircuit | braket.circuits.Circuit: The circuit object.

        Raises:
            TypeError: If the provider is not 'ibm' or 'aws'.
        """
        if provider == 'ibm':
            return self._code_to_circuit_ibm(circuit)
        if provider == 'aws':
            return self._code_to_circuit_aws(circuit)

        raise TypeError("Invalid provider. Expected 'ibm' or 'aws'.")

    def _code_to_circuit_ibm(self, code_str:str) -> qiskit.QuantumCircuit: #Inverse parser to get the circuit object from the string
        """
        Transforms a string representation of a circuit into a Qiskit circuit

        Args:
            code_str (str): The string representation of the Qiskit circuit.
        
        Returns:
            qiskit.QuantumCircuit: The circuit object.
        """
        # Split the code into lines
        try:
            lines = code_str.strip().split('\n')
            # Initialize empty variables for registers and circuit
            qreg = creg = circuit = None
            # Process each line
            for line_index, line in enumerate(lines):
                if not line.strip() or 'import' in line:
                    continue
                if 'import' not in line:
                    if "QuantumRegister" in line:
                        qreg_name = line.split('=')[0].strip()
                        num_qubits = int(line.split('(')[1].split(')')[0].split(',')[0].strip())
                        qreg = qiskit.QuantumRegister(num_qubits, qreg_name)
                    elif "ClassicalRegister" in line:
                        creg_name = line.split('=')[0].strip()
                        num_clbits = int(line.split('(')[1].split(')')[0].split(',')[0].strip())
                        creg = qiskit.ClassicalRegister(num_clbits, creg_name)
                    elif "QuantumCircuit" in line:
                        circuit = qiskit.QuantumCircuit(qreg, creg)
                    elif "circuit." in line:
                        if ".c_if(" in line:
                            operation, condition = line.split('.c_if(')
                        elif ".if_test(" in line:
                            condition = line.split('.if_test(')[1].strip(')')
                            operation = None
                        else:
                            operation = line
                            condition = None
                        # Parse gate operations
                        gate_name = None
                        if operation:#if_test lines don't have operation
                            gate_name = operation.split('circuit.')[1].split('(')[0]
                            args = re.split(r'\s*,\s*', operation.split('(', 1)[1].rsplit(')', 1)[0].strip())
                        if gate_name == "measure":
                            qubit = qreg[int(args[0].split('[')[1].strip(']').split('+')[0]) + int(args[0].split('[')[1].strip(']').split('+')[1].strip(') ')) if '+' in args[0] else int(args[0].split('[')[1].strip(']'))]
                            cbit = creg[int(args[1].split('[')[1].strip(']').split('+')[0]) + int(args[1].split('[')[1].strip(']').split('+')[1].strip(') ')) if '+' in args[1] else int(args[1].split('[')[1].strip(']'))]
                            circuit.measure(qubit, cbit)
                        elif gate_name == "barrier":
                            if args[0] == '': #For barrier()
                                circuit.barrier()
                            elif args[0] == qreg.name: #For barrier(qreg)
                                circuit.barrier(*qreg)
                            else: #For barrier(qreg[0], qreg[1], ...)
                                qubits = [qreg[int(arg.split('[')[1].strip(']').split('+')[0]) + int(arg.split('[')[1].strip(']').split('+')[1].strip(') ')) if '+' in arg else int(arg.split('[')[1].strip(']'))] for arg in args if '[' in arg]
                                circuit.barrier(qubits)
                        elif gate_name == "append":
                            gate_type = args[0]
                            args_no_gate = args[1:]
                            if args_no_gate:
                                if args_no_gate[0].startswith('['):
                                    args_no_gate[0] = args_no_gate[0][1:]
                                if args_no_gate[-1].endswith(']'):
                                    args_no_gate[-1] = args_no_gate[-1][:-1]
                            qubits = [qreg[int(arg.split('[')[1].strip(']').split('+')[0]) + int(arg.split('[')[1].strip(']').split('+')[1].strip(') ')) if '+' in arg else int(arg.split('[')[1].strip(']'))] for arg in args_no_gate if '[' in arg]
                            control_qubits = qubits[:-1]
                            target_qubit = qubits[-1]
                            if gate_type == 'mc_x_gate':
                                mcx = qiskit.circuit.library.MCXGate(len(control_qubits))
                                circuit.append(mcx, control_qubits + [target_qubit])
                            elif gate_type == 'mc_y_gate':
                                circuit.sdg(target_qubit)
                                mcx = qiskit.circuit.library.MCXGate(len(control_qubits))
                                circuit.append(mcx, control_qubits + [target_qubit])
                                circuit.s(target_qubit)
                            elif gate_type == 'mc_z_gate':
                                circuit.h(target_qubit)
                                mcx = qiskit.circuit.library.MCXGate(len(control_qubits))
                                circuit.append(mcx, control_qubits + [target_qubit])
                                circuit.h(target_qubit)
                        else:
                            if operation and not condition:#if_test lines don't have operation
                                qubits = [qreg[int(arg.split('[')[1].strip(']').split('+')[0]) + int(arg.split('[')[1].strip(']').split('+')[1].strip(') ')) if '+' in arg else int(arg.split('[')[1].strip(']'))] for arg in args if '[' in arg]
                                params = [eval(arg, {"__builtins__": None, "np": np}, {}) for param_str in args if '[' not in param_str for arg in param_str.split(',')]
                                gate_operation = getattr(circuit, gate_name)(*params, *qubits) if params else getattr(circuit, gate_name)(*qubits)
                            if condition:
                                creg_name, val = condition.split(')')[0].split(',')
                                val = int(val.strip())

                                # Parse classical condition
                                if '[' in creg_name:
                                    index_expr = creg_name.split('[')[1].strip(']')
                                    if '+' in index_expr:
                                        index = int(index_expr.split('+')[0]) + int(index_expr.split('+')[1].strip())
                                    else:
                                        index = int(index_expr)
                                    classical_condition = creg[index]
                                else:
                                    classical_condition = creg

                                if operation is None:  #when the operation is if_test
                                    #Collect all idented operations to handle them after
                                    block_operations = []
                                    current_line_index = line_index
                                    base_indent = len(line) - len(line.lstrip())

                                    i = current_line_index + 1
                                    while i < len(lines) and i < len(lines):
                                        next_line = lines[i]
                                        if not next_line.strip():  #Skip empty lines
                                            i += 1
                                            continue
                                        line_indent = len(next_line) - len(next_line.lstrip())
                                        if line_indent > base_indent:
                                            block_operations.append(next_line.strip())
                                            lines[i] = ""  #Mark lines as processed so they are not processed again
                                            i += 1
                                        else:
                                            break

                                    if self._get_qiskit_version() < 2:
                                        #Qiskit 1 -> apply c_if with all the operations that were obtained in the previous handling
                                        for op_str in block_operations:
                                            gate_op = self._get_gate_operation(op_str, circuit, qreg, creg)
                                            if gate_op:
                                                gate_op.c_if(classical_condition, val)
                                    else:
                                        #Qiskit 2 -> use if_test with all the operations that were obtained in the previous handling
                                        with circuit.if_test((classical_condition, val)):
                                            for op_str in block_operations:
                                                self._get_gate_operation(op_str, circuit, qreg, creg)

                                else:#when the circuit initially has c_if
                                    if self._get_qiskit_version() < 2:
                                        gate_op = self._get_gate_operation(operation, circuit, qreg, creg)
                                        #Qiskit 1 -> use the same operation on c_if
                                        gate_op.c_if(classical_condition, val)
                                    else:
                                        #Qiskit 2 -> if_test with the operation
                                        with circuit.if_test((classical_condition, val)):
                                            # Re-execute the gate operation inside if_test context
                                            self._get_gate_operation(operation, circuit, qreg, creg)

                                    
        except Exception as e:
            raise ValueError("Invalid circuit code") from e
        return circuit
    
    def _get_gate_operation(self, operation_str: str, circuit: qiskit.QuantumCircuit, qreg: qiskit.QuantumRegister, creg: qiskit.ClassicalRegister) -> Union[qiskit.circuit.Instruction, None]:
        """
        Gets a single gate operation from a string representation.

        Args:
            operation_str (str): The string representation of the gate operation.
            circuit (qiskit.QuantumCircuit): The quantum circuit to which the gate operation will be added.
            qreg (qiskit.QuantumRegister): The quantum register containing the qubits.
            creg (qiskit.ClassicalRegister): The classical register containing the bits.

        Returns:
            qiskit.circuit.Instruction | None: The gate operation added to the circuit, or None if the operation is not valid.
        """
        if not operation_str.strip() or 'circuit.' not in operation_str:
            return None

        gate_name = operation_str.split('circuit.')[1].split('(')[0]
        args = re.split(r'\s*,\s*', operation_str.split('(', 1)[1].rsplit(')', 1)[0].strip())

        if gate_name == "measure":
            qubit = qreg[int(args[0].split('[')[1].strip(']').split('+')[0]) + int(args[0].split('[')[1].strip(']').split('+')[1].strip(') ')) if '+' in args[0] else int(args[0].split('[')[1].strip(']'))]
            cbit = creg[int(args[1].split('[')[1].strip(']').split('+')[0]) + int(args[1].split('[')[1].strip(']').split('+')[1].strip(') ')) if '+' in args[1] else int(args[1].split('[')[1].strip(']'))]
            return circuit.measure(qubit, cbit)
        elif gate_name == "barrier":
            if args[0] == '':
                return circuit.barrier()
            elif args[0] == qreg.name:
                return circuit.barrier(*qreg)
            else:
                qubits = [qreg[int(arg.split('[')[1].strip(']').split('+')[0]) + int(arg.split('[')[1].strip(']').split('+')[1].strip(') ')) if '+' in arg else int(arg.split('[')[1].strip(']'))] for arg in args if '[' in arg]
                return circuit.barrier(qubits)
        else:
            qubits = [qreg[int(arg.split('[')[1].strip(']').split('+')[0]) + int(arg.split('[')[1].strip(']').split('+')[1].strip(') ')) if '+' in arg else int(arg.split('[')[1].strip(']'))] for arg in args if '[' in arg]
            params = [eval(arg, {"__builtins__": None, "np": np}, {}) for param_str in args if '[' not in param_str for arg in param_str.split(',')]
            return getattr(circuit, gate_name)(*params, *qubits) if params else getattr(circuit, gate_name)(*qubits)

    def _code_to_circuit_aws(self, code_str:str) -> Circuit: #Inverse parser to get the circuit object from the string
        """
        Transforms a string representation of a circuit into a Braket circuit.

        Args:
            code_str (str): The string representation of the Braket circuit.
        
        Returns:
            braket.circuits.Circuit: The circuit object.
        """
        # Split the code into lines
        try:
            lines = code_str.strip().split('\n')
            # Initialize the circuit
            circuit = braket.circuits.Circuit()
            safe_namespace = {'np': np, 'pi': np.pi}

            # Process each line
            for line in lines:
                if line.startswith("circuit."):
                    # Parse gate operations
                    operation = line.split('circuit.')[1]
                    gate_name = operation.split('(')[0]

                    if gate_name in ['rx', 'ry', 'rz', 'gpi', 'gpi2', 'phaseshift']:
                        # These gates have a parameter
                        args = operation.split('(')[1].strip(')').split(',')
                        target_qubit = int(args[0].split('+')[0]) + int(args[0].split('+')[1].strip(') ')) if '+' in args[0] else int(args[0].strip(') ').strip())
                        angle = eval(args[1], {"__builtins__": None}, safe_namespace)
                        getattr(circuit, gate_name)(target_qubit, angle)
                    elif gate_name in ['xx', 'yy', 'zz'] or 'cphase' in gate_name:
                        # These gates have 2 parameters
                        args = operation.split('(')[1].strip(')').split(',')
                        target_qubits = [int(arg.split('+')[0]) + int(arg.split('+')[1].strip(') ')) if '+' in arg else int(arg.strip(') ').strip()) for arg in args[:-1]]
                        angle = eval(args[-1], {"__builtins__": None}, safe_namespace)
                        getattr(circuit, gate_name)(*target_qubits, angle)
                    elif gate_name == 'ms':
                        # These gates have multiple parameters (3)
                        args = operation.split('(')[1].strip(')').split(',')
                        target_qubits = [int(arg.split('+')[0]) + int(arg.split('+')[1].strip(') ')) if '+' in arg else int(arg.strip(') ').strip()) for arg in args[:-3]]
                        angles = [eval(arg, {"__builtins__": None}, safe_namespace) for arg in args[-3:]]
                        getattr(circuit, gate_name)(*target_qubits, *angles)
                    else:
                        args = operation.split('(')[1].strip(')').split(',')
                        target_qubits = [int(arg.split('+')[0]) + int(arg.split('+')[1].strip(') ')) if '+' in arg else int(arg.strip(') ').strip()) for arg in args if not any(c.isalpha() for c in arg)]
                        #params = [eval(arg, {"__builtins__": None}, safe_namespace) for arg in args if any(c.isalpha() for c in arg)]
                        getattr(circuit, gate_name)(*target_qubits)
        except Exception as e:
            raise ValueError("Invalid circuit code") from e

        return circuit

    def _fetch_circuit(self, circuit:str) -> requests.Response: # Get the content of the github url
        """
        Gets the content of a GitHub URL file.

        Args:
            circuit (str): The GitHub URL containing the circuit that will be analyzed.
        
        Returns:
            requests.Response: The response of the request to the GitHub URL.

        Raises: 
            ValueError: If the URL is not a raw GitHub URL; if the URL is invalid; or if the request times out.
        """
        try:
            parsed_url = urlparse(circuit)
            if parsed_url.netloc != "raw.githubusercontent.com":
                raise ValueError("URL must come from a raw GitHub file")
            github_raw_url_pattern = r'^https://raw\.githubusercontent\.com/.+/.+/.+/.+$'
            if not re.match(github_raw_url_pattern, circuit):
                raise ValueError("Invalid GitHub URL. Expected a URL in the format 'https://raw.githubusercontent.com/user/repo/branch/file'.")
            response = requests.get(circuit, timeout=5.0)
            response.raise_for_status()
            # Get the name of the file
        except requests.exceptions.Timeout as e:
            raise ValueError("Request timed out") from e
        except requests.exceptions.RequestException as e:
            raise ValueError("Invalid URL, error getting URL content") from e
        return response

    def _get_qubits_machine(self, machine, provider):
        """
        Gets the number of qubits of the machine.

        Args:
            machine (str): The machine that will be analyzed.
            provider (str): The provider of the machine. It can be 'ibm', 'aws'.
        
        Returns:
            int: The number of qubits of the machine.

        Raises:
            ValueError: If the machine is not available.
            TypeError: If the provider is invalid.
        """
        if provider == "ibm":
            return _get_qubits_machine_ibm(machine)
        if provider == "aws":
            return _get_qubits_machine_aws(machine)

        raise TypeError("Invalid provider")
    
    def _get_qiskit_version(self):
        """Get the major version of the installed qiskit package.
        
        Returns:
            int: The major version of qiskit, or 1 if the version cannot be determined.
        """
        try:
            import importlib.metadata
            import re
            version = importlib.metadata.version("qiskit")
            major_version = int(re.match(r'^(\d+)\.', version).group(1))
            return major_version
        except (ImportError, AttributeError):
            # Default to version 1 if detection fails
            return 1
    
