import random
import math

city_dist = []
f = open("../../data/rat99.txt","r")
lines = f.readlines()
for line in lines:
    if line=='EOF' :
        break
    newline = line[:-1].split(' ')
    for cord in newline:
        if cord != '':
            x = eval(cord)
            city_dist.append(x)

N = len(city_dist)//3                                                          # N = number of cities


coordinates = []
for i in range(N):
    x_coordinate = city_dist[i*3+1]
    y_coordinate = city_dist[i*3+2]
    coordinates.append((x_coordinate,y_coordinate))
# print(coordinates)
"""
Constructing the cost matrix
"""
def cost(i,j):                                                                 # calculates the cost of travelling from city i to city j 
    (x_i, y_i) = coordinates[i]
    (x_j, y_j) = coordinates[j]
    c = ((x_i - x_j)**2 + (y_i - y_j)**2)**0.5
    return c

cost_matrix = []
for i in range(0, N):                                                        # Calculates the cost matrix (Iska koi fayda nahin dikh raha)
    temp = []                                                                   
    for j in range(0, N):
        c = cost(i,j)
        temp.append(c)
    cost_matrix.append(temp)

# print(cost_matrix)
radius = []
for i in cost_matrix:
    # print(i[50])
    r = math.ceil(i[50])
    radius.append(r)
print(radius)

avg_radius = round(sum(radius)/len(radius))
print(avg_radius)

initial_solution = []
uncovered_cities = coordinates
visited_cities = []
covered_cities = {}

#initial solution i.e. Tour
initial_solution = []

def cost_between_two_cities(city1,city2):                             #calculating the cost between two cities (given their coordinates)
    (x_i,y_i) = city1
    (x_j,y_j) = city2
    c = ((x_i - x_j)**2 + (y_i - y_j)**2)**0.5
    return c

def total_cost_in_solution(Solution):                                   #total cost of Hamiltonian cycle(Solution)
    total_cost = 0
    for i in range(len(Solution)-1):
        c = cost_between_two_cities(Solution[i],Solution[i+1])
        total_cost += c
    total_cost += cost_between_two_cities(Solution[0],Solution[-1])
    return total_cost

def to_insert_best(initial_solution,city_to_insert):                     # to insert city in the solution so that it has minimum increase in cost.
    #note if we insert at beginning or last, then we have to calculate cost between initial city and last city in visited_city list
    #since it is closed hamilton cycle therefore inserting at beginning is same as appending to last
    cost = []
    t = 0

    if len(initial_solution) <2:
        return

    for i in initial_solution[:-1]:    
        if t == 0:
            c = cost_between_two_cities(city_to_insert,i) + cost_between_two_cities(city_to_insert,initial_solution[len(initial_solution)-1])
            cost.append(c)
        else:
            c = cost_between_two_cities(initial_solution[t-1],city_to_insert)+cost_between_two_cities(city_to_insert,i)
            cost.append(c)
        t+=1

    c_index = cost.index(max(cost))
    if c_index == 0:
        initial_solution.append(city_to_insert)
    else:
        initial_solution.insert(c_index,city_to_insert)        