import random
import networkx as nx
import config
from fitness import calc_fitness, calc_cost

def influence_function(g, paths):
    new_path = sorted(paths, key=lambda x: (x[2]), reverse=True)
    new_route = []
    alternative_route = [p for p in nx.all_shortest_paths(g, new_path[0][0], new_path[0][1])]
    if len(alternative_route) > 1:
        #print(alternative_route)
        for i, j in enumerate(alternative_route):
            cost = calc_cost(g, j)
            source = alternative_route[i][0]
            target = alternative_route[i][1]
            new_route.append([source, target, cost])
            if new_route[i][2] < new_path[0][2]:
                new_path[0] = new_route[i]
            else:
                print(new_route[i][2])
                print(new_path[0][2])
    else:
        print("Não existem rotas alternativas para o PATH mais ocupado")
    return new_path