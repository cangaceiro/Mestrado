import datetime as dt
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pprint
import demand_generator # Funcao que criei para demanda
import itertools
import fitness
import roulletweel_selection
import Mutation
import influence_function
import pandas as pd
from random import randint
from config import *
#import dataset
import utils


g = nx.read_gml('GML_USA/AttMpls.gml') # cultural

g2 = nx.read_gml('GML_USA/AttMpls.gml') # dijkstra

g3 = nx.read_gml('GML_USA/AttMpls.gml') # genético

dijkstra_distances = {node: {} for node in g.nodes}

for i in g.nodes:
    for j in g.nodes:
        if i == j:
            continue
        # Setando os melhores caminhos de um nó para cada nó
        dijkstra_distances[i][j] = list(nx.all_shortest_paths(g, i, j))

# Inicializando Uso da Banda
for edge in g.edges:
    g[edge[0]][edge[1]]['LinkSpeedUsed'] = 0

for edge in g2.edges:
    g2[edge[0]][edge[1]]['LinkSpeedUsed'] = 0

for edge in g3.edges:
    g3[edge[0]][edge[1]]['LinkSpeedUsed'] = 0

ocupacao_media = []
ocupacao_media_lib = []
ocupacao_media_genetico = []

for i in range(CYCLES):
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
    cromossomo_cultural = Mutation.mutation(g, result[1])
    cromossomo_genetico = Mutation.mutation(g3, result[1], cultural=False)
    print('----------------------------------')
    print("POPULAR DEMANDA")
    demand_generator.populate_demand(g, cromossomo_cultural, [d[2] for d in demanda])
    demand_generator.populate_demand(g2, caminhos_dijkstra, [d[2] for d in demanda])
    demand_generator.populate_demand(g3, cromossomo_genetico, [d[2] for d in demanda])

    # if i >= 1:
    #     influence_function.influence_function(g, ocupacao_media[-1])

    ocupacao_media.append(utils.topology_std_desviation(g))
    ocupacao_media_lib.append(utils.topology_std_desviation(g2))
    ocupacao_media_genetico.append(utils.topology_std_desviation(g3))


uso_genetico = []
uso_cultural = []
uso_spf = []
destinos = []
origens = []
for edge in g.edges:
    origens.append(edge[0])
    destinos.append(edge[1])
    uso_spf.append(g3[edge[0]][edge[1]]['LinkSpeedUsed'])
    uso_cultural.append(g[edge[0]][edge[1]]['LinkSpeedUsed'])
    uso_genetico.append(g2[edge[0]][edge[1]]['LinkSpeedUsed'])

usage_df = pd.DataFrame(
    {
        'origem': origens,
        'destino': destinos,
        'SPF': uso_spf,
        'Genético': uso_genetico,
        'Cultural': uso_cultural,
    }
)
usage_df.to_csv(
    'dados/{}.csv'.format(dt.datetime.now().strftime('%Y-%m-%d-%H:%M')),
    index=False
)

print("------------- GRÁFICO ------------------")

ocupacao_df = pd.DataFrame(
    {
        'cultural': ocupacao_media,
        'dijkstra': ocupacao_media_lib,
        'genetico': ocupacao_media_genetico,
    }
)
ocupacao_df.to_csv(
    'dados/{}-desvio.csv'.format(dt.datetime.now().strftime('%Y-%m-%d-%H:%M')),
)

# fig = plt.figure(1, figsize=(9, 6))

# ax = fig.add_subplot(111)

# bp = ax.boxplot([ocupacao_media, ocupacao_media_genetico, ocupacao_media_lib])

# plt.title('Ocupação Média')

# plt.ylabel('Desvio Padrão da Ocupação')

# ax.set_xticklabels(['Ocupação Cultural', 'Ocupação Genética', 'Ocupação SPF'])

# plt.show()

# filename = 'plots/{}.png'.format(dt.datetime.now().strftime('%Y-%m-%d-%H:%M'))

# fig.savefig(filename, dpi=fig.dpi)

# plt.close()

# X = list(range(1, CYCLES + 1))

# fig = plt.figure(1, figsize=(9, 6))

# ax = fig.add_subplot(111)

# ax.plot(X, ocupacao_media, 'r:')
# ax.plot(X, ocupacao_media_lib, 'b-.')
# ax.plot(X, ocupacao_media_genetico, 'g-')

# ax.legend(['Cultural', 'Networkx', 'Genético'])

# plt.show()

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