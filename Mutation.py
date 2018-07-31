import random
import networkx as nx

from config import *

from fitness import calc_fitness, calc_cost
import utils


def mutation(g, chromosome, espaco_crenca=None):
    cultural = not espaco_crenca is None
    if cultural:
        print("ALGORITMO CULTURAL")
    else:
        print("ALGORITMO GENÉTICO")
    chromosome = list(chromosome)
    costs = [calc_cost(g, path) for path in chromosome]
    indexes = []
    indexes_force_mutation = []
    index_quantity = int(max(len(chromosome) * MUTATION_TAX, 1))
    if cultural:
        espaco_crenca_percentual = len(espaco_crenca) / len(g.edges)
        cultural_mutation_tax = MUTATION_TAX + (0.25 * espaco_crenca_percentual)
        index_quantity = int(max(
            len(chromosome) * cultural_mutation_tax, 1
        ))
        for index in range(index_quantity):
            for edge_str in espaco_crenca:
                i = utils.check_edge_chromosome(edge_str, chromosome)
                if i is not None:
                    print("Edge mais usado sendo escolhido", edge_str)
                    indexes.append(i)
                    break
        if len(indexes) < index_quantity:
            indexes_force_mutation = [j for j in range(len(chromosome)) if j not in indexes]
            random.shuffle(indexes_force_mutation)
            indexes.extend(indexes_force_mutation[:index_quantity - len(indexes)])
    else:
        indexes = [i for i in range(len(chromosome))]
        random.shuffle(indexes)
        indexes = indexes[:int(index_quantity)]
    genes = [chromosome[i] for i in indexes]
    mutations = []
    for i_gene, gene in enumerate(genes):
        print('Gene Original', gene)
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
        mutation_node_index = gene.index(mutation_node)
        original_path = gene[mutation_node_index:]
        initial_path = gene[:mutation_node_index]
        target = gene[-1]
        paths = nx.all_simple_paths(g, mutation_node, target)
        paths = sorted(paths, key=len)
        alternative_path = None
        for path in paths:
            if cultural and len(espaco_crenca) > 0:
                for edge_str in espaco_crenca:
                    if not utils.check_edge_path(edge_str, path) and path != original_path:
                        alternative_path = path
                        break    
            elif path != original_path:
                alternative_path = path
                break
        if alternative_path is None:
            print("Não existe outro caminho para este GENE")
        else:
            alternative_path = initial_path + alternative_path
            print('Alternative Path', alternative_path)
            original_path = initial_path + original_path
            if i_gene in indexes_force_mutation:
                mutations.append((original_path, alternative_path))
                print("MUTAÇÃO FORÇADA")
            else:
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
