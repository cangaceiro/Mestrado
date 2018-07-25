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

# g = nx.read_gml('Geant2012.gml')
g = nx.read_gml('Geant2012.gml')
# pos = nx.spring_layout(g, dim=2)
pos = nx.kamada_kawai_layout(g)
nx.draw_networkx_nodes(g,pos,nodelist=nx.nodes(g),node_color='r',node_size=350,alpha=0.8)

#Definir largura do edge(futuro)
#edgebandwith=[c['LinkSpeed'] for (a,b,c) in g.edges(data=True)]
nx.draw_networkx_edges(
    g, pos, edgelist=nx.edges(g), width=1, alpha=1.0,
    edge_color='b', style='solid', arrows=False,
)
nx.draw_networkx_labels(g,pos)
nx.draw(g,pos)
#x,y=pos['NL']
#plt.text(x,y+0.1,s='some text', bbox=dict(facecolor='red', alpha=0.5),horizontalalignment='center')
plt.show()