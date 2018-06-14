#!/usr/bin/env python

import networkx as nx
import matplotlib.pyplot as plt
import pprint
import demand_generator # Funcao que criei para demanda
import itertools
import fitness
import roulletweel_selection
import Mutation
import influence_function
import pandas as pd
from random import randint
import config
import dataset
import utils

g = nx.read_gml('Geant2012.gml')

g2 = nx.read_gml('Geant2012.gml')

dijkstra_distances = {node: {} for node in g.nodes}

for i in g.nodes:
    for j in g.nodes:
        if i == j:
            continue
        dijkstra_distances[i][j] = list(nx.all_shortest_paths(g, i, j))

for edge in g.edges:
    g[edge[0]][edge[1]]['LinkSpeedUsed'] = 0
    g[edge[0]][edge[1]]['Information'] = 0.1

for edge in g2.edges:
    g2[edge[0]][edge[1]]['LinkSpeedUsed'] = 0
    g2[edge[0]][edge[1]]['Information'] = 0.1

ocupacao_media = []
ocupacao_media_lib = []

for i in range(config.CYCLES):
    demanda = demand_generator.generator(list(g.nodes))
    print('DEMANDA')
    print(demanda)
    print('----------------------------------')
    caminhos = []
    caminhos_dijkstra = []

    for item in demanda:
        caminhos.append(dijkstra_distances[item[0]][item[1]])
        caminhos_dijkstra.append(list(nx.shortest_path(g2, item[0], item[1])))

    todas_possibilidades = itertools.product(*caminhos)

    fitness_cromossomos = []

    for cromossomo in todas_possibilidades:
        fitness_cromossomos.append((fitness.calc_fitness(g, cromossomo), cromossomo))

    result = roulletweel_selection.roullet_wheel(fitness_cromossomos)
    print('ESCOLHA')
    cromossomo = Mutation.mutation(g, result[1])
    print('----------------------------------')
    print("POPULAR DEMANDA")
    demand_generator.populate_demand(g, cromossomo, [d[2] for d in demanda])
    demand_generator.populate_demand(g2, caminhos_dijkstra, [d[2] for d in demanda])
    
    ocupacao_media.append(utils.topology_std_desviation(g))
    ocupacao_media_lib.append(utils.topology_std_desviation(g2))

fig = plt.figure(1, figsize=(9, 6))

ax = fig.add_subplot(111)

bp = ax.boxplot([ocupacao_media, ocupacao_media_lib])

plt.title('Ocupação Média')

plt.ylabel('Valores em Gbps')

ax.set_xticklabels(['Ocupação Média Genética', 'Ocupação Média'])

plt.show()

plt.close()

# Plotar Topologia
# pos = nx.spring_layout(g, dim=2)
# nx.draw_networkx_nodes(
#     g, pos, nodelist=nx.nodes(g), node_color='r', node_size=350, alpha=0.8
# )

# #Definir largura do edge(futuro)
# edgebandwith = [c['LinkSpeed'] for (a, b, c) in g.edges(data=True)]
# lambda_color = lambda usage: ((usage > 0.6) and 'r') or 'b'
# colors = [lambda_color(c['LinkSpeedUsed']) for (a, b, c) in g.edges(data=True)]
# nx.draw_networkx_edges(
#     g, pos, edgelist=nx.edges(g), width=1,
#     alpha=1.0, edge_color=colors, style='solid', arrows=False
# )
# nx.draw_networkx_labels(g, pos)
# nx.draw(g,pos)
# plt.title('Topologia Completa')
# plt.show()