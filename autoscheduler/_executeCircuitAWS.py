"""
Module containing AWS execution functions
"""

from braket.devices import LocalSimulator
from braket.aws import AwsDevice
from braket.devices import LocalSimulator
from braket.aws import AwsDevice
from braket.aws.aws_quantum_task import AwsQuantumTask
from braket.circuits import Circuit
from typing import Optional
import time


def _recover_task_result(task_load: AwsQuantumTask) -> dict:
    """
    Waits for the task to complete and recovers the results of the circuit execution.

    Args:
        task_load (braket.aws.aws_quantum_task.AwsQuantumTask): The task to recover the results from.
    
    Returns:
        dict: The results of the circuit execution.
    """
    # recover task
    sleep_times = 0
    while sleep_times < 100000:
        status = task_load.state()
        # wait for job to complete
        # terminal_states = ['COMPLETED', 'FAILED', 'CANCELLED']
        if status == 'COMPLETED':
            # get results
            return task_load.result()
        else:
            time.sleep(1)
            sleep_times = sleep_times + 1
    print("Quantum execution time exceded")
    return None

def _runAWS(machine:str, circuit:Circuit, shots:int, s3_bucket: Optional[tuple] = None) -> dict:
    """
    Executes a circuit in the AWS cloud.

    Args:
        machine (str): The machine to execute the circuit. It can be either a name or an ARN.
        circuit (braket.circuits.Circuit): The circuit to execute.
        shots (int): The number of shots to execute the circuit.
        s3_bucket (tuple, optional): The name of the S3 bucket to store the results. Only needed when `machine` is not 'local'
    
    Returns:
        dict: The results of the circuit execution.

    Raises:
        ValueError: If the machine is not available on the AWS account.
    """
    x = int(shots)

    if machine=="local":
        device = LocalSimulator()
        result = device.run(circuit, shots=x).result()
        counts = result.measurement_counts
        return counts
    
    #Check if the machine is available, also if the user used a name, it changes machine to the ARN of the device
    available_devices = AwsDevice.get_devices()
    available_devices_names = [device.name for device in available_devices]
    available_devices_arn = [device.arn for device in available_devices]
    if machine not in available_devices_names and machine not in available_devices_arn:
        raise ValueError(f"Machine {machine} not available.")
    else:
        if machine in available_devices_names:
            machine = available_devices[available_devices_names.index(machine)].arn
        device = AwsDevice(machine)

    if "sv1" not in machine and "tn1" not in machine:
        task = device.run(circuit, s3_bucket, shots=x, poll_timeout_seconds=5 * 24 * 60 * 60)
        counts = _recover_task_result(task).measurement_counts
        return counts
    else:
        task = device.run(circuit, s3_bucket, shots=x)
        counts = task.result().measurement_counts
        return counts

def _get_qubits_machine_aws(machine):
    """
    Returns the number of qubits of the selected AWS machine.

    Args:
        machine (str): The machine to get the number of qubits from.
    
    Returns:
        int: The number of qubits of the selected machine.

    Raises:
        ValueError: If the machine is not available on the AWS account.
    """
    if machine == 'local':
        device = LocalSimulator()
    else:
        available_devices = AwsDevice.get_devices()
        available_devices_names = [device.name for device in available_devices]
        available_devices_arn = [device.arn for device in available_devices]
        if machine not in available_devices_names and machine not in available_devices_arn:
            raise ValueError(f"Machine {machine} not available.")
        else:
            if machine in available_devices_names:
                machine = available_devices[available_devices_names.index(machine)].arn
            device = AwsDevice(machine)
    return device.properties.dict()['paradigm']['qubitCount']