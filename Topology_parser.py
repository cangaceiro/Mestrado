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
    g[edge[0]][edge[1]]['LinkSpeedUsed'] = 0.001

for edge in g2.edges:
    g2[edge[0]][edge[1]]['LinkSpeedUsed'] = 0.001

for edge in g3.edges:
    g3[edge[0]][edge[1]]['LinkSpeedUsed'] = 0.001

ocupacao_media = []
ocupacao_media_lib = []
ocupacao_media_genetico = []
fitness_spf = []
fitness_genetico = []
fitness_cultural = []
edge_usage = []
espaco_crenca = []
demandas = []

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
    
    demandas.append(sum([i[2] for i in demanda]))

    todas_possibilidades = itertools.product(*caminhos)
    fitness_cromossomos = []

    for cromossomo in todas_possibilidades:
        fitness_cromossomos.append((fitness.calc_fitness(g, cromossomo), cromossomo))

    result = roulletweel_selection.roullet_wheel(fitness_cromossomos)
    print('ESCOLHA')
    cromossomo_genetico = Mutation.mutation(g3, result[1])
    cromossomo_cultural = Mutation.mutation(g, result[1], espaco_crenca)
    print('----------------------------------')
    print("POPULAR DEMANDA")
    demand_generator.populate_demand(g, cromossomo_cultural, [d[2] for d in demanda])
    demand_generator.populate_demand(g2, caminhos_dijkstra, [d[2] for d in demanda])
    demand_generator.populate_demand(g3, cromossomo_genetico, [d[2] for d in demanda])
    fitness_genetico.append(fitness.calc_fitness(g3, cromossomo_genetico))
    fitness_spf.append(fitness.calc_fitness(g2, caminhos_dijkstra))
    fitness_cultural.append(fitness.calc_fitness(g, cromossomo_cultural))
    # if i >= 1:
    #     influence_function.influence_function(g, ocupacao_media[-1])

    ocupacao_media.append(utils.topology_std_desviation(g))
    ocupacao_media_lib.append(utils.topology_std_desviation(g2))
    ocupacao_media_genetico.append(utils.topology_std_desviation(g3))
    for edge in g.edges:
        edge_usage.append(
            (i, edge[0], edge[1], g[edge[0]][edge[1]]['LinkSpeedUsed'],
            g2[edge[0]][edge[1]]['LinkSpeedUsed'], g3[edge[0]][edge[1]]['LinkSpeedUsed'])
        )
        uso_edge_cultural = (
            g[edge[0]][edge[1]]['LinkSpeedUsed'] / float(g[edge[0]][edge[1]]['LinkSpeed'])
        )
        if uso_edge_cultural > 0.3:
            edge_str = '{}-{}'.format(edge[0], edge[1])
            if not edge_str in espaco_crenca: 
                espaco_crenca.append(edge_str)
    espaco_crenca = utils.rank_espaco_crenca(espaco_crenca, g)
    if len(espaco_crenca):
        print("Edge mais usado:", espaco_crenca[0])
    # if i == 29:
    #     import ipdb; ipdb.set_trace()
    

data_hora = dt.datetime.now().strftime('%Y-%m-%d-%H:%M')

print('--------------- SALVAMENTO DEMANDA ------------')
demanda_df = pd.DataFrame(
    {
        'geracao': list(range(CYCLES)),
        'demanda': demandas,
    }
)
demanda_df.to_csv(
    'dados/{}-demanda.csv'.format(data_hora), index=False
)


print('--------------- ESPAÇO DE CRENÇA ------------')
print('TOTAL: {}'.format(len(espaco_crenca)))
print(espaco_crenca)


uso_genetico = []
uso_cultural = []
uso_spf = []
destinos = []
origens = []
for usage in edge_usage:
    origens.append(usage[1])
    destinos.append(usage[2])
    uso_cultural.append(usage[3])
    uso_spf.append(usage[4])
    uso_genetico.append(usage[5])

usage_df = pd.DataFrame(
    edge_usage, columns=['ciclo', 'origem', 'destino', 'Cultural', 'SPF', 'Genético']
)
usage_df.to_csv(
    'dados/{}-uso.csv'.format(data_hora), index=False
)


fitness_df = pd.DataFrame(
    {
        'Fitness SPF': fitness_spf,
        'Fitness Genético': fitness_genetico,
        'Fitness Cultural': fitness_cultural,
    }
)
fitness_df.to_csv(
    'dados/{}-fitness.csv'.format(data_hora), index=False
)

ocupacao_df = pd.DataFrame(
    {
        'cultural': ocupacao_media,
        'dijkstra': ocupacao_media_lib,
        'genetico': ocupacao_media_genetico,
    }
)
ocupacao_df.to_csv(
    'dados/{}-desvio.csv'.format(data_hora), index=False
)

# print("------------- GRÁFICO ------------------")

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