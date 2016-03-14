# -*- coding: utf-8 -*-

import random
import math
import sys
import copy

def get_random_edge(graph):
    """
    >>> a, b = get_random_edge({ 1: [2, 3, 4], 2: [1], 3: [1], 4: [1] })
    >>> a <= 4 and b <= 4
    True

    :param graph:
    :return:
    """
    random_vertex = random.choice(list(graph.keys()))
    random_adjacent_vertex = random.choice(graph[random_vertex])

    return random_vertex, random_adjacent_vertex

def contract_graph(G, u, v):
    """
    >>> contract_graph({ 1: [2, 3], 2: [1, 3, 4], 3: [1, 2, 4], 4: [2, 3] }, 1, 3)
    {2: [5, 5, 4], 4: [2, 5], 5: [2, 2, 4]}

    :param G:
    :param u:
    :param v:
    :return:
    """

    u_adjacency = G[u]
    v_adjacency = G[v]

    sorted_graph_keys = list(G.keys())
    sorted_graph_keys.sort()
    w = sorted_graph_keys[-1] + 1

    # rewrite adjacency list from u & v removing reference to each other
    G[w] = list(filter(lambda x: True if x not in [u, v] else False, u_adjacency + v_adjacency))
    del G[u]
    del G[v]

    for vertex in G:
        for idx, adjacent_vertex in enumerate(G[vertex]):
            if adjacent_vertex == u or adjacent_vertex == v:
                G[vertex][idx] = w

    return G

def get_min_cut(G, **kwargs):
    """

    """
    random.seed()

    while len(G.keys()) > 2:
        u, v = get_random_edge(G)
        contract_graph(G, u, v)

    key = list(G.keys())[0]

    return len(G[key])


def get_randomized_min_cut(G):
    """
    >>> get_randomized_min_cut({ 1: [2, 3], 2: [1, 3, 4], 3: [1, 2, 4], 4: [2, 3] })
    2

    >>> get_randomized_min_cut({ 1: [2, 5, 6], 2: [1, 3, 5], 3: [2, 4, 8], 4: [3, 7, 8], 5: [1, 2, 6], 6: [1, 5, 7], 7: [4, 6, 8], 8: [3, 4, 7]})
    2

    :param G:
    :return:
    """
    n = len(G)
    trials = int(n ** 2 * math.log1p(n))
    min_cut = sys.maxsize
    last_percent = 0

    for trial in range(0, trials):
        # Uncomment to see progress
        #
        # percent = trial / float(trials)
        # if percent - last_percent > 0.01:
        #     print("%d%% (%d) " % (percent * 100, trial))
        #     last_percent = percent

        G_clone = copy.deepcopy(G)
        trail_min_cut = get_min_cut(G_clone)
        if trail_min_cut < min_cut:
            min_cut = trail_min_cut

    return min_cut


def get_graph_from_file(path):
    graph = {}

    with open(path, 'r') as raw_input_data:
        for line in raw_input_data:
            col = list(map(int, line.strip().split('\t')))
            graph[col[0]] = col[1:]

    return graph

if __name__ == '__main__':
    import doctest
    import sys

    print('recursionlimit: ', sys.getrecursionlimit())
    sys.setrecursionlimit(11000)

    doctest.testmod()

    path = 'kargerMinCut.txt'
    course_graph = get_graph_from_file(path)
    course_graph_min_cut = get_randomized_min_cut(course_graph)
    print(course_graph_min_cut)