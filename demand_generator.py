import random

def generator(nodes):
    demand=[]
    Drange=random.randint(1,10)# gerar total de demandas
    for i in range(Drange):
        source=random.choice(nodes) #Definir o Source
        cp_nodes= list(nodes)# copiar a lista
        cp_nodes.remove(source)#Remover o source da copia da lista
        target=random.choice(cp_nodes)#escolher o target da lista sem o source
        demand.append([source,target,random.randint(10, 500)/1000])# Gerar ocupação aleatoria e converter em GIGA
    return demand


def populate_demand(g, cromossomo, usage):
    assert len(cromossomo) == len(usage), \
        "tamanho do uso (demanda) deve ser igual ao tamanho do cromossomo"
    for i in range(len(cromossomo)):
        gene = cromossomo[i]
        current = gene[0]
        for j in range(1, len(gene)):
            link_speed_used = g[current][gene[j]]['LinkSpeedUsed']
            g[current][gene[j]]['LinkSpeedUsed'] = link_speed_used + usage[i]
            current = gene[j]
