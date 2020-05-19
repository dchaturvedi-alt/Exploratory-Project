from initialization import total_cost_in_solution,uncovered_cities,visited_cities,to_insert_best,initial_solution,cost_between_two_cities,avg_radius,covered_cities
import random

"""
These datas as per given for experiment
"""
Prob_cross = 0.66
Prob_fm = 0.25

Solution_Sample =[]

for i in range(50):
    s = True
    while s:
        
        if len(uncovered_cities) == 0:
            s = False
            break
        rand = random.randint(0,len(uncovered_cities)-1)
        v_city = uncovered_cities.pop(rand)
        visited_cities.append(v_city)

        temp_uncovered_cities = uncovered_cities

        #To insert at partially constructed tour Start-->
        if len(visited_cities) > 2:
            to_insert_best(initial_solution,v_city)
        else:
            initial_solution.append(v_city)
        #<-- End --> 
        z=0
        cover_cities = []
        for i in temp_uncovered_cities:
            c = cost_between_two_cities(v_city,i)
            if c < avg_radius:
                c_city = uncovered_cities.pop(z)
                cover_cities.append(c_city)
            else:
                z+=1

        covered_cities[v_city] = cover_cities

    Solution_Sample.append(initial_solution)

S_collection = list(Solution_Sample)
print(S_collection)

total_cost_collection = []
for i in range(len(S_collection)):
    c = total_cost_in_solution(S_collection[i])
    total_cost_collection.append(c)

indu = total_cost_collection.index(max(total_cost_collection))

S_best = S_collection[indu]

def Binary_Tournament(S_collection):
    size = len(S_collection)
    random_binary_selection = random.sample(S_collection,2)
    print(random_binary_selection)

    fitness1 = total_cost_in_solution(random_binary_selection[0])
    fitness2 = total_cost_in_solution(random_binary_selection[1])

    if fitness1 >fitness2:
        return random_binary_selection[0]
    else:
        return random_binary_selection[1]


#Outputing the child by crossover function taking parents.
def crossover(parent_1, parent_2):
    def fill_with_parent1_genes(child, parent, genes_n):
        print(child,'from fill with parent1 genes')
        start_at = random.randint(0, len(parent)-genes_n-1)
        finish_at = start_at + genes_n
        for i in range(start_at, finish_at):
            child[i] = parent_1[i]

    def fill_with_parent2_genes(child, parent):
        print(child,'from fill with parent2 genes')
        j = 0
        for i in range(0, len(parent)):
            if i == len(child):
                return
            if child[i] == None:
                while parent[j] in child:
                    j += 1
                child[i] = parent[j]
                j += 1

    genes_n = len(parent_1)
    child = [None for _ in range(genes_n)]
    fill_with_parent1_genes(child, parent_1, genes_n // 2)
    fill_with_parent2_genes(child, parent_2)

    print(child,"child")

    while child[-1] == None:
        child.pop(-1)

    print(child,"child")    

    return child

def mutate(Parent, rate):
    for _ in range(len(Parent)):
        if random.random() < rate:
            sel_genes = random.sample(Parent, 2)
            a = Parent.index(sel_genes[0])
            b = Parent.index(sel_genes[1])
            Parent[b], Parent[a] = Parent[a], Parent[b]    

    return Parent

cost_list = []

w = True
ginti =0
while w:
    u01 = random.random()
    if u01<Prob_cross:
        P1 = Binary_Tournament(S_collection)
        P2 = Binary_Tournament(S_collection)
        C = crossover(P1,P2)    
    else:
        P = Binary_Tournament(S_collection)
        # if(u01 < Prob_fm):
        C = mutate(P,0.5)

    # C = LS2N(C)
    if total_cost_in_solution(C) > total_cost_in_solution(S_best):
        # C = GE(C)
        S_best = C
    
    kimat = total_cost_in_solution(S_best)
    cost_list.append(kimat)
    if ginti == 29:
        w = False
    ginti+=1


nInstance = len(cost_list)
Best_cost = max(cost_list)
Average_cost = sum(cost_list)/nInstance
Deviation = Best_cost-Average_cost

f = open("output_CSP_GA.txt","a")
f.write("\t"+"Instance"+"\t"+"Best cost"+"\t"+"Average cost"+"\t"+"Deviation"+"\t"+"nInstance"+"\n")
f.write("\t"+"rat99"+"\t"+str(Best_cost)+"\t"+str(Average_cost)+"\t"+str(Deviation)+"\t"+str(nInstance)+"\n")
f.close()