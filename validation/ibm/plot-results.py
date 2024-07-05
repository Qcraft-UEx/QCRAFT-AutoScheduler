from matplotlib import pyplot as plt
import os
import glob
import ast
import math

def calculate_hellinger_distance(dist1, dist2):
    sum_of_squares = 0
    #Get all unique keys from both distributions
    all_keys = set(dist1.keys()).union(set(dist2.keys()))
    for key in all_keys: #For each key if it doesnt exist in the other distribution, the probability of that element is set to 0
        p = dist1.get(key, 0)
        q = dist2.get(key, 0)
        sum_of_squares += (math.sqrt(p) - math.sqrt(q)) ** 2 #Calculate the squared difference between the square roots of the probabilities
    return math.sqrt(sum_of_squares / 2) #Calculate the Hellinger distance by taking the square root of half the sum of squared differences

def plot_individual_algorithm(all_distances):
    #Gets the current file to create the folder if not exists
    base_dir = 'plot/algorithm'
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(current_file_dir, base_dir)
    os.makedirs(base_dir, exist_ok=True)

    for key, distances in all_distances.items():
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)

        ax.boxplot([distances])
        ax.set_xticklabels([])
        #ax.set_ylim(0,1)
        
        ax.set_title(f'Hellinger Distance for {key}')
        ax.set_ylabel('Hellinger Distance')
        ax.set_xlabel(f'{key}')
        plt.xticks(rotation=45)
        plt.tight_layout()

        filename = os.path.join(base_dir, f'{key}.png')
        plt.savefig(filename, bbox_inches='tight')
        plt.close()

def plot_and_save(all_distances):
    base_dir='plot'
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(current_file_dir, base_dir)
    os.makedirs(base_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(20, 10))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    #Create a box plot for each algorithm
    num_boxes = len(all_distances.values())
    positions = [1 + 0.5 * i for i in range(num_boxes)]
    ax.boxplot(all_distances.values(), tick_labels=all_distances.keys(), widths=0.5, positions=positions)

    ax.set_title('Hellinger Distance for each algorithm')
    ax.set_ylabel('Hellinger Distance')
    ax.set_xlabel('Algorithm')
    plt.xticks(rotation=45)  #Rotate the x-axis labels for better readability
    plt.tight_layout()
    #Sets filename and saves the flot
    filename = os.path.join(base_dir, 'hellinger.png')
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

def counts_to_probabilities(data_dict):
    #Gets the total number and sets its probability to each key
    total_count = sum(data_dict.values())
    return {key: value / total_count for key, value in data_dict.items()}

def handle_file(dir):
    dist = {}
    for filepath in glob.glob(os.path.join(dir, "*.txt")):
        with open(filepath, 'r') as file:
            key = os.path.splitext(os.path.basename(filepath))[0]
            content_dict = ast.literal_eval(file.read())
            #Convert frequencies into probaiblity distributions to use the hellinger distance
            dist[key] = counts_to_probabilities(content_dict)

    return dist
            
def load_data(autoscheduled_dir_name, individual_dir_name):
    scheduled = {}
    individual = {}
    scheduled_list = []

    #Get the directory of the current file
    current_file_dir = os.path.dirname(os.path.abspath(__file__))

    #Obtain the directories of the different results
    autoscheduled_dir = os.path.join(current_file_dir, autoscheduled_dir_name)

    #Load data from autoscheduled
    for item in os.listdir(autoscheduled_dir):
        item_path = os.path.join(autoscheduled_dir, item)
        if os.path.isdir(item_path):
            scheduled = handle_file(item_path)
            scheduled_list.append(scheduled)

    individual_dir = os.path.join(current_file_dir, individual_dir_name)
    #Load data from individual
    individual = handle_file(individual_dir)

    return scheduled_list, individual

def plot_dict(scheduled_dicts, individual):

    all_distances = {}#To store all distances per algorithm

    for key in individual:
        distances = []
        for scheduled in scheduled_dicts:
            if key in scheduled:
                #Gets the hellinger distance of individual vs every scheduled result and saves it to plot them
                distance = calculate_hellinger_distance(individual[key], scheduled[key])
                distances.append(distance)
        if distances:  #If distance is not empty
            all_distances[key] = distances
    
    plot_individual_algorithm(all_distances)
    plot_and_save(all_distances)
    

individual = {}
scheduled_dicts = []
scheduled_dicts, individual = load_data('autoscheduled', 'individual')
plot_dict(scheduled_dicts, individual)
