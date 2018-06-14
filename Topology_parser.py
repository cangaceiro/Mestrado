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

MUTATION_TAX = 0.1

global MUTATION_TAX

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

db = dataset.connect('sqlite:///db.sqlite3')
db['media_ocupacao'].delete()
db['media_ocupacao_sem_cultural'].delete()
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
    #========Plotagem sem algoritmo Cultural========
    valores_ocupacao_sem_cultural = []
    paths = []
    for edge in g.edges:
        print(edge[0], edge[1], g[edge[0]][edge[1]]['LinkSpeedUsed'])
        paths.append([edge[0], edge[1], g[edge[0]][edge[1]]['LinkSpeedUsed']])
    for i in paths:
        valores_ocupacao_sem_cultural.append(i[2])
    valores_sem_cultural = pd.Series(valores_ocupacao_sem_cultural)
    media_sem_cultural = valores_sem_cultural.mean()
    #####Salvado no banco de dados para gerar media############
    
    media_sem_cultural_table = db['media_ocupacao_sem_cultural']
    media_sem_cultural_table.insert({'media': media_sem_cultural})
    db.commit()

ocupacao_media = [i['media'] for i in db['media_ocupacao_sem_cultural'].all()]
# ocupacao_media_cultural = [i['media'] for i in db['media_ocupacao'].all()]

fig, ax = plt.subplots()
plt.boxplot(ocupacao_media)
plt.title('Ocupação Média')
plt.ylabel('Valores em Gbps')
ax.set_xticklabels(['Ocupação Média', 'Ocupação Média Cultural'])
plt.show()
plt.close()
