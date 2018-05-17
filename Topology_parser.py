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


g=nx.read_gml('Geant2012.gml')

#pos=nx.spring_layout(g,dim=2)
#nx.draw_networkx_nodes(g,pos,nodelist=nx.nodes(g),node_color='r',node_size=350,alpha=0.8)
#
# #Definir largura do edge(futuro)
# #edgebandwith=[c['LinkSpeed'] for (a,b,c) in g.edges(data=True)]
#nx.draw_networkx_edges(g,pos,edgelist=nx.edges(g),width=1,alpha=1.0,edge_color='b',style='solid',arrows=False)
#nx.draw_networkx_labels(g,pos)
#nx.draw(g,pos)
# #x,y=pos['NL']
# #plt.text(x,y+0.1,s='some text', bbox=dict(facecolor='red', alpha=0.5),horizontalalignment='center')
#plt.title('Topologia Completa')
#plt.show()
# path=has_path(g,17,30)
# print(path)


dijkstra_distances = {node: {} for node in g.nodes}

for i in g.nodes:
    for j in g.nodes:
        if i == j:
            continue
        dijkstra_distances[i][j] = list(nx.all_shortest_paths(g, i, j))


'''for source in dijkstra_distances:
    print("Source:", source)
    for target in dijkstra_distances[source]:
        print("Target:", target)
        pprint.pprint([path for path in dijkstra_distances[source][target]])'''

for edge in g.edges:
    g[edge[0]][edge[1]]['LinkSpeedUsed'] = 0
    g[edge[0]][edge[1]]['Information'] = 0.1

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
    print('----------------------------------')
    '''rotas_escolhidas = []
    for i in result[1]:
        rotas_escolhidas.append([i[0], i[-1]])
    print("ORIGEM E DESTINO DE CADA ESCOLHA:", rotas_escolhidas)
    print('----------------------------------')
    rotas_possiveis_da_escolha = []
    for j in rotas_escolhidas:
        rotas_possiveis_da_escolha.append(([j[0], j[-1], [p for p in nx.all_shortest_paths(g, j[0], j[-1])]]))
    print("ROTAS POSSIVEIS PARA CADA ESCOLHA:", rotas_possiveis_da_escolha)
    print('----------------------------------')'''
    print("POPULAR DEMANDA")
    demand_generator.populate_demand(g, result[1], [d[2] for d in demanda])
    paths = []
    for edge in g.edges:
        print(edge[0], edge[1], g[edge[0]][edge[1]]['LinkSpeedUsed'])
        paths.append([edge[0], edge[1], g[edge[0]][edge[1]]['LinkSpeedUsed']])
    print('-------------Mutacao---------------------')
    print(Mutation.mutation(g, paths))
    print('############################################ OUTRO PATH ##################################################################')
    '''c = []
    print("OCUPACÃO DOS LINKS")
    for j in range(len(result[1])):
        b = [(v, result[1][j][i + 1]) for i, v in enumerate(result[1][j]) if (i + 1) < len(result[1][j])]
        c.append(b)
    founds = []
    print(c)
    print(paths)
    for val1, val2, val3 in paths:
        for i in range(len(c)):
            if ((val1, val2) in c[i]): #creditos de Thyago
                founds.append([val1, val2, val3])
            else:
                if ((val2, val1) in c[i]):
                    founds.append([val1, val2, val3])
    print(founds)'''

#import os

#os.environ['PYTHONINSPECT'] = 'True'
