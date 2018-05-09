from Topology_parser import *

def mutation():
    print(rotas_possiveis_da_escolha)
    for i, j in enumerate(rotas_possiveis_da_escolha):
        if len(j[2]) > 1:
            rotas_possiveis_da_escolha[i] = j[2]

    print(rotas_possiveis_da_escolha)
        #print(i[2])
        #print(len(i[2]))

    #print([i for i in rotas_possiveis_da_escolha[0][2]])
    return
print(mutation())