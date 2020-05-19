import utils
import random
import argparse
import tsp_ga as ga
from datetime import datetime

def run(args):
    genes = utils.get_genes_from(args.cities_fn)

    if args.verbose:
        print("-- Running TSP-GA with {} cities --".format(len(genes)))

    history = ga.run_ga(genes, args.pop_size, args.n_gen,
                        args.tourn_size, args.mut_rate, args.verbose)
    print(ga.cost_list)

    if args.verbose:
        print("-- Drawing Route --")

    # utils.plot(history['cost'], history['route'])

    if args.verbose:
        print("-- Done --")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose', type=int, default=1)
    parser.add_argument('--pop_size', type=int, default=500, help='Population size')
    parser.add_argument('--tourn_size', type=int, default=50, help='Tournament size')
    parser.add_argument('--mut_rate', type=float, default=0.02, help='Mutation rate')
    parser.add_argument('--n_gen', type=int, default=20, help='Number of equal generations before stopping')
    parser.add_argument('--cities_fn', type=str, default="../../data/rat99.txt", help='Data containing the geographical coordinates of cities')

    random.seed(datetime.now())
    args = parser.parse_args()

    if args.tourn_size > args.pop_size:
        raise argparse.ArgumentTypeError('Tournament size cannot be bigger than population size.')


    # nInstance = len(ga.cost_list)
    # Best_cost = max(ga.cost_list)
    # Average_cost = sum(ga.cost_list)/nInstance
    # Deviation = Best_cost-Average_cost

    # f = open("../data/output.txt","a")
    # print(args.pop_size)
    # f.write("\nGA Parameters: Population Size: "+str(args.pop_size)+" Tournament size: "+str(args.tourn_size)+" Mutation Rate: "+str(args.mut_rate)+" Number of genes: "+str(args.n_gen)
        # +"\n")
    # f.write("\t"+"Instance"+"\t"+"Best cost"+"\t"+"Average cost"+"\t"+"Deviation"+"\t"+"nInstance"+"\n")
    # f.write("\t"+"rat99"+"\t"+Best_cost+"\t"+Average_cost+"\t"+Deviation+"\t"+nInstance+"\n")
    # f.close()

    run(args)