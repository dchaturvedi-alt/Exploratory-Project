import matplotlib.pyplot as plt
import tsp_ga as ga
import pandas as pd
from random import sample
# from mpl_toolkits.basemap import Basemap
    # import cartopy
    # import cartopy.feature as cpf


def get_genes_from(fn, sample_n=0):
    # df = pd.read_csv(fn)
    genes = []
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

    N = len(city_dist)//3

    for i in range(N):
        g = ga.Gene(str(city_dist[i*3]),city_dist[i*3+1],city_dist[i*3+2])
        genes.append(g)

    # genes = [ga.Gene(row['city'], row['latitude'], row['longitude'])
    #          for _, row in df.iterrows()]
    # #chaging here
    # for _, row in df.iterrows():
    #     print(ga.Gene(row['city'],row['latitude'], row['longitude']))
    #     print(row['longitude'])

    #change

    return genes if sample_n <= 0 else sample(genes, sample_n)

def plot(costs, individual, save_to=None):
    plt.figure(1)
    plt.subplot(121)
    plot_ga_convergence(costs)

    plt.subplot(122)
    # plot_route(individual)

    if save_to is not None:
        plt.savefig(save_to)
        plt.close()
    else:
        plt.show()

def plot_ga_convergence(costs):
    x = range(len(costs))
    plt.title("GA Convergence")
    plt.xlabel('generation')
    plt.ylabel('cost (KM)')
    plt.text(x[len(x) // 2], costs[0], 'min cost: {} KM'.format(costs[-1]), ha='center', va='center')
    plt.plot(x, costs, '-')


# def plot_route(individual):
#     # m = Basemap(projection='lcc', resolution=None,
#     #             width=5E6, height=5E6,
#     #             lat_0=-15, lon_0=-56)

#     #Change
#     # m = plt.gca(projection=cartopy.crs.PlateCarree())
#     #Change
#     plt.axis('off')
#     plt.title("Shortest Route")

#     for i in range(0, len(individual.genes)):
#         print(individual.genes[i].lng,individual.genes[i].lat)
#         x, y = m(individual.genes[i].lng, individual.genes[i].lat)

#         plt.plot(x, y, 'ok', c='r', markersize=5)
#         if i == len(individual.genes) - 1:
#             x2, y2 = m(individual.genes[0].lng, individual.genes[0].lat)
#         else:
#             x2, y2 = m(individual.genes[i+1].lng, individual.genes[i+1].lat)

#         plt.plot([x, x2], [y, y2], 'k-', c='r')