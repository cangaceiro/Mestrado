import random
import networkx as nx

from config import *

from fitness import calc_fitness, calc_cost


def mutation(g, chromosome, espaco_crenca=None):
    cultural = not espaco_crenca is None
    if cultural:
        print("ALGORITMO CULTURAL")
    else:
        print("ALGORITMO GENÉTICO")
    chromosome = list(chromosome)
    costs = [calc_cost(g, path) for path in chromosome]
    indexes = []
    index_quantity = max(len(chromosome) * MUTATION_TAX, 1)
    if cultural:
        espaco_crenca_percentual = len(espaco_crenca) / len(g.edges)
        if espaco_crenca_percentual > 0.1:
            index_quantity = max(
                len(chromosome) * (MUTATION_TAX + espaco_crenca_percentual), 1
            )
        costs = enumerate(costs)
        costs = sorted(costs, key=lambda i: i[1])[:-1]
        indexes = [i[0] for i in costs[:int(index_quantity)]]
    else:
        indexes = [i for i in range(len(chromosome))]
        random.shuffle(indexes)
        indexes = indexes[:int(index_quantity)]
    genes = [chromosome[i] for i in indexes]
    mutations = []
    for gene in genes:
        if len(gene) < 3:
            continue
        if cultural:
            edges = []
            for i, node in enumerate(gene):
                if (i + 1) < len(gene):
                    edges.append((node, gene[i + 1]))
            edge = sorted(
                edges, key=lambda e: g[e[0]][e[1]]['LinkSpeedUsed']
            )[-1]
            mutation_node = edge[0]
        else:
            mutation_node = random.choice(gene[1:len(gene) - 1])
        print(mutation_node)
        mutation_node_index = gene.index(mutation_node)
        original_path = gene[mutation_node_index:]
        initial_path = gene[:mutation_node_index]
        target = gene[-1]
        paths = nx.all_simple_paths(g, mutation_node, target)
        paths = sorted(paths, key=len)
        alternative_path = None
        for path in paths:
            if path != original_path:
                alternative_path = path
                break
        if alternative_path is None:
            print("Não existe outro caminho para este GENE")
        else:
            alternative_path = initial_path + alternative_path
            original_path = initial_path + original_path
            original_path_cost = calc_cost(g, original_path)
            alternative_path_cost = calc_cost(g, alternative_path)
            print("Custo Original:", original_path_cost)
            print("Custo Alternativo:", alternative_path_cost)
            if alternative_path_cost < original_path_cost:
                mutations.append((original_path, alternative_path))
    print("Mutações")
    print(mutations)
    for m in mutations:
        original_path = m[0]
        alternative_path = m[1]
        original_path_index = chromosome.index(original_path)
        chromosome[original_path_index] = alternative_path
    return chromosome
