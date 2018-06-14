import pandas as pd


def topology_std_desviation(g):
    usage = []    
    for edge in g.edges:
        usage.append(g[edge[0]][edge[1]]['LinkSpeedUsed'])
    return pd.Series(usage).std()
