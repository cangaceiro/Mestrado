import random
import networkx as nx
import config
from fitness import calc_fitness, calc_cost
from utils import topology_std_desviation

def influence_function(g, std_old):
    std_desviation_old = std_old
    std_desviation_new = topology_std_desviation(g)
    if std_desviation_new >= std_desviation_old:
        MUTATION_TAX = MUTATION_TAX + 0.01
    if MUTATION_TAX > 0.2:
        MUTATION_TAX = 0.2