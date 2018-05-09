import networkx as nx
import matplotlib.pyplot as plt
G=nx.path_graph(3)

pos=nx.spring_layout(G)

nx.draw(G,pos)
x,y=pos[1]


plt.text(x,y+0.1,s='some text', bbox=dict(facecolor='red', alpha=0.5),horizontalalignment='center')