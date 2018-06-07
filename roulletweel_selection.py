import random

def roullet_wheel(cromossomos):
    """
    :param cromossomos: Tupla de dois elementos, onde o primeiro é o fitness e o segundo é uma lista com o path completo
    :return:
    """
    total_fitness = sum([c[0] for c in cromossomos])
    roleta = random.random() * total_fitness
    for c in cromossomos:
        if c[0] > roleta:
            return c
        else:
            roleta = roleta - c[0]
