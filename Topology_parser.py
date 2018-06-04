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
import pymysql

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
    #========Plotagem sem algoritmo Cultural========
    valores_ocupacao_sem_cultural = []
    for i in paths:
        valores_ocupacao_sem_cultural.append(i[2])
    valores_sem_cultural = pd.Series(valores_ocupacao_sem_cultural)
    media_sem_cultural = valores_sem_cultural.mean()
    #####Salvado no banco de dados para gerar media############
    base_de_dados = pymysql.connect("localhost", "root", "123456", "base_de_dados_mestrado_thyago")
    cursor = base_de_dados.cursor()
    cursor_1 = base_de_dados.cursor()
    cursor.execute("INSERT INTO media_ocupacao_sem_cultural VALUES (NULL, %s)", ((str(media_sem_cultural))))
    cursor_1.execute("SELECT media FROM media_ocupacao_sem_cultural")
    valores_plotagem_sem_cultural = []
    for i in list(cursor_1):
        for j in i:
            valores_plotagem_sem_cultural.append(j)
    ocupacao_media_temp = map(float, valores_plotagem_sem_cultural)
    ocupacao_media_temp_1 = [k * 10 for k in ocupacao_media_temp]
    ocupacao_media = ocupacao_media_temp_1
    base_de_dados.commit()
    base_de_dados.close()
    ###########################################
    plt.boxplot(ocupacao_media)
    plt.title('Ocupação Média utilizando Dijkstra')
    plt.ylabel('Valores em Gbps')
    plt.xticks([1], ['Ocupacao média da rede'])
    plt.show()
    plt.close()

    #===============================================
    print('-------------PLOTAGEM COM CULTURAL---------------------')
    #print(Mutation.mutation(g, influence_function.influence_function(paths)))
    valores_ocupacao = []
    media = []
    for i in Mutation.mutation(g, influence_function.influence_function(paths)):
        valores_ocupacao.append(i[2])
    valores = pd.Series(valores_ocupacao)
    media = valores.mean()
    #####Salvado no banco de dados para gerar media############
    base_de_dados = pymysql.connect("localhost", "root", "123456", "base_de_dados_mestrado_thyago")
    cursor = base_de_dados.cursor()
    cursor_1 = base_de_dados.cursor()
    cursor.execute("INSERT INTO media_ocupacao VALUES (NULL, %s)", ((str(media))))
    cursor_1.execute("SELECT media FROM media_ocupacao")
    valores_plotagem = []
    for i in list(cursor_1):
        for j in i:
            valores_plotagem.append(j)
    ocupacao_media_temp = map(float, valores_plotagem)
    ocupacao_media_temp_1 = [k*10 for k in ocupacao_media_temp]
    ocupacao_media = ocupacao_media_temp_1
    base_de_dados.commit()
    base_de_dados.close()
    ###########################################
    plt.boxplot(ocupacao_media)
    plt.title('Ocupação Média utilizando Algoritmo Cultural')
    plt.ylabel('Valores em Gbps')
    plt.xticks([1], ['Ocupacao média da rede'])
    plt.show()
    plt.close()
    print('############################################ OUTRO PATH ##################################################################')

#import os
#os.environ['PYTHONINSPECT'] = 'True'
