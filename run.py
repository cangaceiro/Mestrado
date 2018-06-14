#!/usr/bin/env python

import networkx as nx
import matplotlib.pyplot as plt
import pprint
import demand_generator # Funcao que criei para demanda
import itertools
import fitness
import roulletweel_selection
import Mutation

from random import randint

g = nx.read_gml('Geant2012.gml')

dijkstra_distances = {node: {} for node in g.nodes}

for i in g.nodes:
    for j in g.nodes:
        if i == j:
            continue
        dijkstra_distances[i][j] = list(nx.all_shortest_paths(g, i, j))

for edge in g.edges:
    g[edge[0]][edge[1]]['LinkSpeedUsed'] = 0

for i in range(1):
    demanda = demand_generator.generator(list(g.nodes))
    print('DEMANDA')
    print(demanda)
    print('----------------------------------')
    caminhos = []

    for item in demanda:
        caminhos.append(dijkstra_distances[item[0]][item[1]])

    todas_possibilidades = itertools.product(*caminhos)

    fitness_cromossomos = []

    for cromossomo in todas_possibilidades:
        fitness_cromossomos.append((fitness.calc_fitness(g, cromossomo), cromossomo))

    result = roulletweel_selection.roullet_wheel(fitness_cromossomos)
    print('ESCOLHA')
    print(result)
    print('MUTAÇÃO')
    chromosome = Mutation.mutation(g, result[1])
    print('----------------------------------')
    print("POPULAR DEMANDA")
    demand_generator.populate_demand(g, chromosome, [d[2] for d in demanda])
    paths = []
    for edge in g.edges:
        print(edge[0], edge[1], g[edge[0]][edge[1]]['LinkSpeedUsed'])
        paths.append([edge[0], edge[1], g[edge[0]][edge[1]]['LinkSpeedUsed']])
    print('----------------------------------')


import os
os.environ['PYTHONINSPECT'] = 'True'
