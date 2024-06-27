#!/usr/bin/env python
# coding: utf-8

# import libraries

from qiskit import transpile
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def _runIBM(machine:str, circuit:QuantumCircuit, shots:int) -> dict:
    """
    Executes a circuit in the IBM cloud.

    Args:
    machine (str): The machine to execute the circuit.
    circuit (QuantumCircuit): The circuit to execute.
    shots (int): The number of shots to execute the circuit.
    
    Returns:
    dict: The results of the circuit execution.
    """
    if machine == "local":
        backend = AerSimulator()
        x = int(shots)
        job = backend.run(circuit, shots=x)
        result = job.result()
        counts = result.get_counts()
        return counts
    else:
        # Load your IBM Quantum account
        service = QiskitRuntimeService()
        backend = service.backend(machine)
        qc_basis = transpile(circuit, backend)
        x = int(shots)
        job = backend.run(qc_basis, shots=x) 
        result = job.result()
        counts = result.get_counts()
        return counts
