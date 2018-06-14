import random
import networkx as nx
import config


from fitness import calc_fitness, calc_cost


def mutation(g, chromosome):
    chromosome = list(chromosome)
    indexes = []
    index_quantity = max(len(chromosome) * MUTATION_TAX, 1)
    while True:
        index = random.randint(0, len(chromosome) - 1)
        if not index in indexes:
            indexes.append(index)
            index_quantity = index_quantity - 1
        if index_quantity <= 0:
            break
    genes = [chromosome[i] for i in indexes]
    mutations = []
    for gene in genes:
        if len(gene) < 3:
            continue
        mutation_node = random.choice(gene[1:len(gene) - 1])
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
