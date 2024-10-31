"""
Module containing qirk translator functions
"""
import ast
from urllib.parse import unquote

def _get_ibm_individual(ind_circuit:str,d:int) -> str:
    """
    Translates the results of the Quirk URL into a Qiskit circuit, adding a offset to the qubits.

    Args:
        ind_circuit (str): The Quirk URL.
        d (int): The offset to add to the qubits.
    
    Returns:
        str: The Qiskit circuit.
    """
    url = ind_circuit  # Get the 'url' parameter
    circuitos = []
    if url:
        circuit = ast.literal_eval(unquote(url).split('circuit=')[1])
        circuitos.append(circuit)

    code_array = []

    for index, circuito in enumerate(circuitos):
        despl = d
        for j in range(len(circuito['cols'])):
            x = circuito['cols'][j]
            if 'Swap' in x:
                # Handle swap gates
                swap_indices = [k for k, g in enumerate(x) if g == 'Swap']
                if len(swap_indices) == 2:
                    code_array.append(f'circuit.swap(qreg_q[{swap_indices[0]+despl}], qreg_q[{swap_indices[1]+despl}])')
            elif '•' in x:
                # Handle multi-controlled gates
                control_indices = [k for k, g in enumerate(x) if g == '•']
                num_controls = len(control_indices)
                if 'X' in x:
                    target_index = x.index('X')
                    code_array.append(f'mc_x_gate = MCMT(XGate(), {num_controls}, 1)')
                    code_array.append(f'circuit.append(mc_x_gate, [{", ".join([f"qreg_q[{i+despl}]" for i in control_indices])}, qreg_q[{target_index+despl}]])')
                elif 'Z' in x:
                    target_index = x.index('Z')
                    code_array.append(f'mc_z_gate = MCMT(ZGate(), {num_controls}, 1)')
                    code_array.append(f'circuit.append(mc_z_gate, [{", ".join([f"qreg_q[{i+despl}]" for i in control_indices])}, qreg_q[{target_index+despl}]])')
                elif 'Y' in x:
                    target_index = x.index('Y')
                    code_array.append(f'mc_y_gate = MCMT(YGate(), {num_controls}, 1)')
                    code_array.append(f'circuit.append(mc_y_gate, [{", ".join([f"qreg_q[{i+despl}]" for i in control_indices])}, qreg_q[{target_index+despl}]])')
            else:
                for i in range(len(x)):
                    gate = x[i]
                    if gate == 'Measure':
                        code_array.append(f'circuit.measure(qreg_q[{i+despl}], creg_c[{i+despl}])')
                    elif gate == 'H':
                        code_array.append(f'circuit.h(qreg_q[{i+despl}])')
                    elif gate == 'Z':
                        code_array.append(f'circuit.z(qreg_q[{i+despl}])')
                    elif gate == 'X':
                        code_array.append(f'circuit.x(qreg_q[{i+despl}])')
                    elif gate == 'Y':
                        code_array.append(f'circuit.y(qreg_q[{i+despl}])')
                    elif gate == 'X^½':
                        code_array.append(f'circuit.rx(np.pi/2, qreg_q[{i+despl}])')
                    elif gate == 'X^-½':
                        code_array.append(f'circuit.rx(-np.pi/2, qreg_q[{i+despl}])')
                    elif gate == 'X^¼':
                        code_array.append(f'circuit.rx(np.pi/4, qreg_q[{i+despl}])')
                    elif gate == 'X^-¼':
                        code_array.append(f'circuit.rx(-np.pi/4, qreg_q[{i+despl}])')
                    elif gate == 'Y^½':
                        code_array.append(f'circuit.ry(np.pi/2, qreg_q[{i+despl}])')
                    elif gate == 'Y^-½':
                        code_array.append(f'circuit.ry(-np.pi/2, qreg_q[{i+despl}])')
                    elif gate == 'Y^¼':
                        code_array.append(f'circuit.ry(np.pi/4, qreg_q[{i+despl}])')
                    elif gate == 'Y^-¼':
                        code_array.append(f'circuit.ry(-np.pi/4, qreg_q[{i+despl}])')
                    elif gate == 'Z^½':
                        code_array.append(f'circuit.s(qreg_q[{i+despl}])')
                    elif gate == 'Z^-½':
                        code_array.append(f'circuit.sdg(qreg_q[{i+despl}])')
                    elif gate == 'Z^¼':
                        code_array.append(f'circuit.t(qreg_q[{i+despl}])')
                    elif gate == 'Z^-¼':
                        code_array.append(f'circuit.tdg(qreg_q[{i+despl}])')

    code_string = '\n'.join(code_array)
    return code_string


def _get_aws_individual(ind_circuit:str, d:int) -> str:
    """
    Translates the results of the Quirk URL into a Braket circuit, adding a offset to the qubits.

    Args:
        ind_circuit (str): The Quirk URL.
        d (int): The offset to add to the qubits.
    
    Returns:
        str: The Braket circuit.
    """
    url = ind_circuit
    circuitos = []
    if url:
        circuit = ast.literal_eval(unquote(url).split('circuit=')[1])
        circuitos.append(circuit)

    code_array = []

    for index, circuito in enumerate(circuitos):
        despl = d

        for j in range(len(circuito['cols'])):
            x = circuito['cols'][j]
            if 'Swap' in x:
                # Handle swap gates
                swap_indices = [k for k, g in enumerate(x) if g == 'Swap']
                if len(swap_indices) == 2:
                    code_array.append('circuit.swap('+str(swap_indices[0]+despl)+', '+str(swap_indices[1]+despl)+')')
            elif '•' in x:
                # Handle multi-controlled gates
                control_indices = [k for k, g in enumerate(x) if g == '•']
                first_index = control_indices[0]
                if 'X' in x:
                    target_index = x.index('X')
                    code_array.append('circuit.cnot('+str(first_index+despl)+', '+str(target_index+despl)+')')
                elif 'Z' in x:
                    target_index = x.index('Z')
                    code_array.append('circuit.cz('+str(first_index+despl)+', '+str(target_index+despl)+')')
                elif 'Y' in x:
                    target_index = x.index('Y')
                    code_array.append('circuit.cy('+str(first_index+despl)+', '+str(target_index+despl)+')')
            else:
                for i in range(len(x)):
                    if x[i] == 'H':
                        code_array.append('circuit.h('+str(i+despl)+')')
                    elif x[i] == 'Z':
                        code_array.append('circuit.z('+str(i+despl)+')')
                    elif x[i] == 'Y':
                        code_array.append('circuit.y('+str(i+despl)+')')
                    elif x[i] == 'X':
                        code_array.append('circuit.x('+str(i+despl)+')')
                    elif x[i] == 'X^½':
                        code_array.append('circuit.rx('+str(i+despl)+', np.pi/2)')
                    elif x[i] == 'X^-½':
                        code_array.append('circuit.rx('+str(i+despl)+', -np.pi/2)')
                    elif x[i] == 'X^¼':
                        code_array.append('circuit.rx('+str(i+despl)+', np.pi/4)')
                    elif x[i] == 'X^-¼':
                        code_array.append('circuit.rx('+str(i+despl)+', -np.pi/4)')
                    elif x[i] == 'Y^½':
                        code_array.append('circuit.ry('+str(i+despl)+', np.pi/2)')
                    elif x[i] == 'Y^-½':
                        code_array.append('circuit.ry('+str(i+despl)+', -np.pi/2)')
                    elif x[i] == 'Y^¼':
                        code_array.append('circuit.ry('+str(i+despl)+', np.pi/4)')
                    elif x[i] == 'Y^-¼':
                        code_array.append('circuit.ry('+str(i+despl)+', -np.pi/4)')
                    elif x[i] == 'Z^½':
                        code_array.append('circuit.s('+str(i+despl)+')')
                    elif x[i] == 'Z^-½':
                        code_array.append('circuit.si('+str(i+despl)+')')
                    elif x[i] == 'Z^¼':
                        code_array.append('circuit.t('+str(i+despl)+')')
                    elif x[i] == 'Z^-¼':
                        code_array.append('circuit.ti('+str(i+despl)+')')

    code_string = '\n'.join(code_array)
    return code_string
