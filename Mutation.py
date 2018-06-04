import random
import networkx as nx
import config
import influence_function
import numpy as np
from fitness import calc_fitness, calc_cost
from random import choice

def mutation(g, chromosome):
    new_path = chromosome
    new_route = []
    alternative_route_temp = [p for p in nx.all_simple_paths(g, new_path[0][0], new_path[0][1])]
    if len(alternative_route_temp) > 1:
        alternative_route = [choice(alternative_route_temp)]
        for i, j in enumerate(alternative_route):
            cost = calc_cost(g, j)
            source = alternative_route[i][0]
            target = alternative_route[i][1]
            new_route.append([source, target, cost])
            if new_route[i][2] < new_path[0][2]:
                new_path[0] = new_route[i]
            else:
                print("O novo caminho é mais custoso que o anterior, caminho anterior preservado.")
    else:
        print("Não existem rotas alternativas para o PATH mais ocupado")
    return chromosome
