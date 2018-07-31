import statistics


def topology_std_desviation(g):
    usage = []    
    for edge in g.edges:
        usage.append(g[edge[0]][edge[1]]['LinkSpeedUsed'])
    return statistics.stdev(usage)


def rank_espaco_crenca(espaco_crenca, g):
    def calc_uso_edge(edge_str):
        edge = edge_str.split('-')
        return (
            g[edge[0]][edge[1]]['LinkSpeedUsed'] / float(g[edge[0]][edge[1]]['LinkSpeed'])
        )
    return sorted(espaco_crenca, key=calc_uso_edge, reverse=True)

def check_edge_chromosome(edge, chromosome):
    for i, gene in enumerate(chromosome):
        if check_edge_path(edge, gene):
            return i
    return None
                        

def check_edge_path(edge, path):
    nodes = edge.split('-')
    try:
        index_source = path.index(nodes[0])
        index_target = path.index(nodes[1])
        return abs(index_source - index_target) == 1
    except ValueError:
        return False
