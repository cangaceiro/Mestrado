import random
import networkx as nx
import config

from fitness import calc_fitness


def mutation(g, chromosome):
    indexes = []
    index_quantity = max(len(chromosome) * config.MUTATION_TAX, 1)
    while True:
        index = random.randint(0, len(chromosome) - 1)
        if not index in indexes:
            indexes.append(index)
            index_quantity = index_quantity - 1
        if index_quantity < 0:
            break
    print("INDEXES -- MUTATION")
    print(indexes)
    genes = [chromosome[i] for i in indexes]
    for gene in genes:
        if len(gene) < 3:
            continue
        print("GENE")
        print(gene)
        mutation_node = random.choice(gene[1:len(gene) - 1])
        print(mutation_node)
        target = gene[-1]
        paths = nx.all_shortest_paths(g, mutation_node, target)
        for path in paths:
            print(path)
    return chromosome
