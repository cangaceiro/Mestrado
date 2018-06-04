import random
import networkx as nx
import config
from fitness import calc_fitness, calc_cost

def influence_function(paths):
    new_path = sorted(paths, key=lambda x: (x[2]), reverse=True)
    return new_path