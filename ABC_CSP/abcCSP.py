
# bees.py
# A solution to the Traveling Salesman Problem
# that mimics the foraging behavior of honey bees


import csv
import math
import random
import sys
from scipy.spatial import distance

class Bee:
    def __init__(self, node_set):
        self.role = ''
        self.path = list(node_set) # stores all nodes in each bee, will randomize foragers
        self.distance = 0
        self.cycle = 0 # number of iterations on current solution


def read_data_from_csv(file_name):
    """
    Returns data read from file.
    """
    data_list = []
    with open(file_name) as f:
        reader = csv.reader(f)
        data_list = [[int(eval(s)) for s in row.split(',')] for row in f]
    return data_list


def get_distance_between_nodes(n1, n2):
    """
    Calculates the Euclidean distance between two nodes.
    """
    return distance.euclidean(n1, n2)


def make_distance_table(data_list):
    """
    Creates a table that stores distance between every pair of nodes.
    """
    length = len(data_list)
    table = [[get_distance_between_nodes(
        (data_list[i][1],data_list[i][2]), (data_list[j][1],data_list[j][2]))
        for i in range(0, length)] for j in range(0, length)]
    return table


def get_total_distance_of_path(path, table):
    """
    Calculates the total distance of an individual bee's path.
    Terminates at starting node to complete cycle.
    """
    # Creates a copy of path, puts head at end of list.
    # Zip lists to create pairs of neighbor coords,
    # will create a cycle that terminates at starting node.
    new_path = list(path)
    new_path.insert(len(path), path[0])
    new_path = new_path[1:len(new_path)]

    coordinates = zip(path, new_path)
    distance = sum([table[i[0]][i[1]] for i in coordinates])
    return round(distance, 3)


def new_path(data):
    vis = [0 for x in data]
    n = len(data)
    cnt = 0
    path = []
    """
    To calculate the average radius we find the centroid of the distribution and find the maximum distance of a point from centroid.
    """
    sum_x = 0
    sum_y = 0
    for x in data:
        sum_x += x[1]
        sum_y += x[2]
    avg_x = sum_x/len(data)
    avg_y = sum_y/len(data)
    radius = 0
    for x in data:
        radius = max(radius, get_distance_between_nodes((x[1],x[2]), (avg_x, avg_y)))
    radius = radius/2.5
    while cnt < n:
        city = random.randint(0,n-1)
        if vis[city]==0:
            vis[city] = 1
            cnt += 1
            path.append(city)
            for x in data:
                if get_distance_between_nodes((data[city][1],data[city][2]), (x[1], x[2])) <= radius and vis[x[0]]==0:
                    vis[x[0]] = 1
                    cnt += 1
    
    return path
    
def initialize_hive(population, data):
    """
    Initializes a hive and populates it with bees.
    Bees will have a randomized path attribute.
    """
    path = new_path(data)

    hive = [Bee(path) for i in range (0, population)]
    
    return hive


def assign_roles(hive, role_percentiles, table):
    """
    Assigns initial roles based on role percentiles
    to each bee in the hive.
    Assigns randomized path to forager bees.
    """
    population = len(hive)
    onlooker_count = math.floor(population * role_percentiles[0])
    forager_count = math.floor(population * role_percentiles[1])

    for i in range(0, onlooker_count):
        hive[i].role = 'O'

    for i in range(onlooker_count, (onlooker_count + forager_count)):
        hive[i].role = 'F'
        random.shuffle(hive[i].path)
        hive[i].distance = get_total_distance_of_path(hive[i].path, table)

    return hive

def mutate_path(path):
    """
    Gets a random index 0 to next to last element.
    Copies path, swaps two nodes, compares distance.
    Returns mutated path.
    """
    # - will go out of range if last element is chosen.
    random_idx = random.randint(0, len(path) - 2)
    new_path = list(path)
    new_path[random_idx], new_path[random_idx + 1] = new_path[random_idx + 1], new_path[random_idx]
    return new_path

def forage(bee, table, limit):
    """
    Worker bee behavior, iteratively refines a potential shortest path
    by swapping randomly selected neighbor indices.
    """
    new_path = mutate_path(bee.path)
    new_distance = get_total_distance_of_path(new_path, table)

    if new_distance < bee.distance:
        bee.path = new_path
        bee.distance = new_distance
        bee.cycle = 0 # reset cycle so bee can continue to make progress
    else:
        bee.cycle += 1
    if bee.cycle >= limit: # if bee is not making progress
        bee.role = 'S'
    return bee.distance, list(bee.path)


def scout(bee, table):
    """
    Scout bee behavior, abandons unsuccessful path for new random path.
    Resets role to forager.
    """
    new_path = list(bee.path)
    random.shuffle(new_path)
    bee.path = new_path
    bee.distance = get_total_distance_of_path(new_path, table)
    bee.role = 'F'
    bee.cycle = 0


def waggle(hive, best_distance, table, forager_limit, scout_count):
    """
    Captures results from work of forager bees,
    chooses new random path for scouts to explore,
    returns results for overlookers to assess.
    """
    best_path = []
    results = []

    for i in range(0, len(hive)):
        if hive[i].role == 'F':
            distance, path = forage(hive[i], table, forager_limit)
            if distance < best_distance:
                best_distance = distance
                best_path = list(hive[i].path)
            results.append((i, distance))

        elif hive[i].role == 'S':
            scout(hive[i], table)

    # after processing all bees, set worst performers to scout
    results.sort(reverse = True, key=lambda tup: tup[1])
    scouts = [ tup[0] for tup in results[0:int(scout_count)] ]
    for new_scout in scouts:
        hive[new_scout].role = 'S'
    return best_distance, best_path


def recruit(hive, best_distance, best_path, table):
    """
    Recruits onlooker bees to iterate on best soluction so far.
    Returns updated best_distance, best_path.
    """
    for i in range(0, len(hive)):
        if hive[i].role == 'O':
            new_path = mutate_path(best_path)
            new_distance = get_total_distance_of_path(new_path, table)
            if new_distance < best_distance:
                best_distance = new_distance
                best_path = new_path
    return best_distance, best_path

def make_csv(data, file_name):
    """
    Writes data to csv file.
    """
    with open(file_name, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)
    f.close()

cost_list = []

def main():
    # Control parameters
    population = 180
    forager_percent = 0.5
    onlooker_percent = 0.5
    role_percent = [onlooker_percent, forager_percent]
    scout_percent = 0.2
    scout_count = math.ceil(population * scout_percent)
    forager_limit = 500
    cycle_limit = 25
    cycle = 1

    # Data source
    data = read_data_from_csv("../../data/rat99.csv")

    # Global vars
    best_distance = sys.maxsize
    
    
    # Initialization
    table = make_distance_table(data)
    hive = initialize_hive(population, data)
    assign_roles(hive, role_percent, table)

    avg = 0
    while cycle < cycle_limit:
        waggle_distance, waggle_path = waggle(hive, best_distance, table, forager_limit, scout_count)
        if waggle_distance < best_distance:
            best_distance = waggle_distance
            best_path = list(waggle_path)
            
        recruit_distance, recruit_path = recruit(hive, best_distance, best_path, table)
        if recruit_distance < best_distance:
            best_distance = recruit_distance
            best_path = list(recruit_path)
        
        avg += best_distance
        cycle += 1

    avg = avg/cycle_limit
    print(avg)
    cost_list.append(avg)


#------------------------------------------------------------------------------------#

if __name__ == '__main__':
    for i in range (0, 30):
        main()
    nInstance = len(cost_list)
    Best_cost = max(cost_list)
    Average_cost = sum(cost_list)/nInstance
    Deviation = Best_cost-Average_cost


    with open("output_ABC_CSP.txt","a") as f:
        # f.write("\t"+"Instance"+"\t"+"Best cost"+"\t"+"Average cost"+"\t"+"Deviation"+"\t"+"nInstance"+"\n")
        f.write("\t"+"att532"+"\t"+str(Best_cost)+"\t"+str(Average_cost)+"\t"+str(Deviation)+"\t"+str(nInstance)+"\n")
        f.close()