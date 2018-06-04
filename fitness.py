import random
import config


def calc_fitness(g, cromossomo):
    fitness = 0
    for caminho in cromossomo:
        fitness = fitness + (1 / calc_cost(g, caminho))
    return fitness


def calc_cost(g, caminho):
    cost = 0
    current = caminho[0]
    for i in range(1, len(caminho)):
        link_speed_used = g[current][caminho[i]]['LinkSpeedUsed']
        link_speed = float(g[current][caminho[i]]['LinkSpeed'])
        information = g[current][caminho[i]]['Information']
        cost = cost + (0.0000001 + (link_speed_used / link_speed))
        current = caminho[i]
    return cost
