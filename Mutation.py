import random
import networkx as nx
import config

from fitness import calc_fitness, calc_cost

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
    mutations = []
    for gene in genes:
        if len(gene) < 3:
            continue
        print("GENE")
        print(gene)
        mutation_node = random.choice(gene[1:len(gene) - 1])
        print(mutation_node)
        mutation_node_index = gene.index(mutation_node)
        original_path = gene[mutation_node_index:]
        target = gene[-1]
        paths = nx.all_shortest_paths(g, mutation_node, target)
        alternative_path = None
        try:
            for path in paths:
                if path != original_path:
                    alternative_path = path
                    break
        except nx.NetworkXNoPath:
            pass
        if alternative_path is None:
            print("Não existe outro caminho para este GENE")
        else:
            original_path_cost = calc_cost(g, original_path)
            alternative_path_cost = calc_cost(g, alternative_path)
            print("Custo Original")
            print(original_path_cost)
            print("Custo Alternativo")
            print(alternative_path_cost)
            if alternative_path <= original_path:
                mutations.append((original_path, alternative_path))
            print("Mutações")
            print(mutations)
    for m in mutations:
        original_path = m[0]
        alternative_path = m[1]
        original_path_index = chromosome.index(original_path)
        chromosome[original_path_index] = alternative_path
    return chromosome
