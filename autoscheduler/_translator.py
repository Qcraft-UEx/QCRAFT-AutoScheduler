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
        despl=d
        for j in range(0, len(circuito['cols'])):

            x=circuito['cols'][j]
            g = [[x.count(z), z] for z in set(x)]

            l=len(g)
            # Check for 'Swap' gates in all columns
            if 'Swap' in x:
                # Find the indices of the 'Swap' gates
                swap_indices = [i for i, gate in enumerate(x) if gate == 'Swap']
                # Perform the swap operation between the qubits at these indices
                for i in range(0, len(swap_indices), 2):  # Iterate over pairs of indices
                    code_array.append('circuit.swap(qreg_q['+str(swap_indices[i]+despl)+'], qreg_q['+str(swap_indices[i+1]+despl)+'])')

            if l==1 or (l==2 and ((g[0][1]=='H' and g[1][1]==1) or (g[0][1]==1 and g[1][1]=='H') or (g[0][1]=='Z' and g[1][1]==1) or (g[0][1]==1 and g[1][1]=='Z') or (g[0][1]=='X' and g[1][1]==1) or (g[0][1]==1 and g[1][1]=='X'))):

                if x[0] == 'Measure':
                    for k in range(0, len(x)):
                        code_array.append('circuit.measure(qreg_q['+str(k+despl)+'], creg_c['+str(k+despl)+'])')
                else:
                    for i in range(0, len(x)):
                        if x[i] == 'H':
                            code_array.append('circuit.h(qreg_q['+str(i+despl)+'])')
                        elif x[i] == 'Z':
                            code_array.append('circuit.z(qreg_q['+str(i+despl)+'])')
                        elif x[i] == 'X':
                            code_array.append('circuit.x(qreg_q['+str(i+despl)+'])')
            elif l==2 or l==3:
                if 'X' in x and '•' in x:
                    code_array.append('circuit.cx(qreg_q['+str(x.index("•")+despl)+'], qreg_q['+str(x.index("X")+despl)+'])')
                elif 'Z' in x and '•' in x:
                    code_array.append('circuit.cx(qreg_q['+str(x.index("•")+despl)+'], qreg_q['+str(x.index("Z")+despl)+'])')

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
        despl=d
        for j in range(0, len(circuito['cols'])):

            x=circuito['cols'][j]
            g = [[x.count(z), z] for z in set(x)]

            l=len(g)
            # Check for 'Swap' gates in all columns
            if 'Swap' in x:
                # Find the indices of the 'Swap' gates
                swap_indices = [i for i, gate in enumerate(x) if gate == 'Swap']
                # Perform the swap operation between the qubits at these indices
                for i in range(0, len(swap_indices), 2):  # Iterate over pairs of indices
                    code_array.append('circuit.swap('+str(swap_indices[i]+despl)+', '+str(swap_indices[i+1]+despl)+')')

            if l==1 or (l==2 and ((g[0][1]=='H' and g[1][1]==1) or (g[0][1]==1 and g[1][1]=='H') or (g[0][1]=='Z' and g[1][1]==1) or (g[0][1]==1 and g[1][1]=='Z') or (g[0][1]=='X' and g[1][1]==1) or (g[0][1]==1 and g[1][1]=='X'))):         
                for i in range(0, len(x)):
                    if x[i] == 'H':
                        code_array.append('circuit.h('+str(i+despl)+')')
                    elif x[i] == 'Z':
                        code_array.append('circuit.z('+str(i+despl)+')')
                    elif x[i] == 'X':
                        code_array.append('circuit.x('+str(i+despl)+')')
            elif l==2 or l==3:
                if 'X' in x and '•' in x:
                    code_array.append('circuit.cnot('+str(x.index("•")+despl)+', '+str(x.index("X")+despl)+')')
                elif 'Z' in x and '•' in x:
                    code_array.append('circuit.cnot('+str(x.index("•")+despl)+', '+str(x.index("Z")+despl)+')')

    code_string = '\n'.join(code_array)
    return code_string

