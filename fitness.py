import random
import config


def calc_fitness(g, cromossomo):
    fitness = 0
    for caminho in cromossomo:
        fitness = fitness + (1 / calc_cost(g, caminho))
    return fitness


def calc_cost(g, caminho):
    cost = 1
    current = caminho[0]
    for i in range(1, len(caminho)):
        link_speed_used = g[current][caminho[i]]['LinkSpeedUsed']
        link_speed = float(g[current][caminho[i]]['LinkSpeed'])
        information = g[current][caminho[i]]['Information']
        usage = (link_speed_used / link_speed)
        if usage <= 0.3:
            usage = usage * 1
        elif usage <= 0.6:
            usage = usage * 1.5
        else:
            usage = usage * 2
        cost = cost + usage
        current = caminho[i]
    return cost
