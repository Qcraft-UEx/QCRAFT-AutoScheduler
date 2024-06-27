def _divideResults(counts:dict, shots:int, provider:str, qb:list, users:list, circuit_name:list) -> list:
    """
    Divides the results of a circuit execution among the users that executed it.

    Args:
    counts (dict): The results of the circuit execution.
    shots (int): The number of shots that the circuit was executed.
    provider (str): The provider of the circuit execution.
    qb (list): The number of qubits of the circuit.
    users (list): The users that executed the circuit.
    circuit_name (list): The name of the circuit that was executed.
    
    Returns:
    list: The results of the circuit execution divided among the users.
    """
    result = []
    for i in range(len(shots)):
        
        newCounts = {}

        for key, value in counts.items(): #Reducing each dictionary so that it contains the useful part of each user
            rightRemovedQubits = sum(qb[0:i])  #Values to remove from the right
            leftRemovedQubits = sum(qb[i+1:len(qb)])  #Values to remove from the left
            if provider == 'aws':
                data = key[rightRemovedQubits:]  #Data is the custom value of each user
                data = data[:(len(data)-leftRemovedQubits)]
                data = data[::-1] #AWS gives the results backwards compared to IBM, to have a standard, the result is reversed
            else:
                data = key[leftRemovedQubits:]  #Data is the custom value of each user
                data = data[:(len(data)-rightRemovedQubits)]
            
            if data in newCounts:
                newCounts[data] += value
            else:
                newCounts[data] = value

        # Calculate the total number of shots
        total_shots = sum(newCounts.values())
        # Check if the total number of shots is equal to the number of executed shots
        selected_counts = newCounts

        result.append({(users[i],circuit_name[i]):selected_counts})

    return result