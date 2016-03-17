# -*- coding: utf-8 -*-

import random
import math
import sys
import copy

def print_err(*args):
    print(*args, file=sys.stderr)


class DfsProperties:
    def __init__(self):
        self.explored = {}
        self.processing_counter = 0
        self.leaders = {}
        self.finishing_times = {}


def dfs_loop(graph_edges, ordering=None):
    """
    >>> props = dfs_loop([(1, 7), (4, 1), (7, 4), (7, 9), (9, 6), (6, 3), (3, 9), (6, 8), (8, 2), (2, 5), (5, 8)])
    >>> props.finishing_times
    {1: 7, 2: 3, 3: 1, 4: 8, 5: 2, 6: 5, 7: 9, 8: 4, 9: 6}

    :param graph_edges:
    :param ordering:
    :return:
    """
    """
    :param graph_edges:
    :param ordering:
    :return:
    """
    props = DfsProperties()
    source_vertex = None

    graph_adjacency_dict = get_adjacency_list(graph_edges)
    max_label = get_max_vertex_label(graph_adjacency_dict)

    if not ordering:
        ordering = range(max_label, 0, -1)

    for vertex_label in ordering:
        if vertex_label not in props.explored or not props.explored[vertex_label]:
            source_vertex = vertex_label
            dfs(graph_adjacency_dict, props, source_vertex, vertex_label)

    return props


def dfs(G, props, source_vertex, vertex):
    explored_dict = props.explored
    leader_dict = props.leaders

    explored_dict[vertex] = True
    leader_dict[vertex] = source_vertex
    vertex_adjacency_list = G.get(vertex, [])

    for head_vertex in vertex_adjacency_list:
        if head_vertex not in explored_dict or not explored_dict[head_vertex]:
            dfs(G, props, source_vertex, head_vertex)

    props.processing_counter += 1
    props.finishing_times[vertex] = props.processing_counter

    return


def get_scc(graph_edges):
    """
    >>> get_scc([(7, 1), (1, 4), (4, 7), (9, 7), (6, 9), (3, 6), (9, 3), (8, 6), (2, 8), (5, 2), (8, 5)])
    [3, 3, 3]

    :param graph_edges:
    :return:
    """

    inv_graph_edges = get_inverted_graph(graph_edges)
    print_err("DFS first pass...")
    dfs_first_pass_props = dfs_loop(inv_graph_edges)
    finishing_times = dfs_first_pass_props.finishing_times

    magical_ordering = sorted(finishing_times, key=lambda vertex: finishing_times[vertex], reverse=True)

    print_err("DFS second pass...")

    dfs_second_pass_props = dfs_loop(graph_edges, magical_ordering)

    leaders_for_vertex = dfs_second_pass_props.leaders

    scc_sizes = {}
    for vertex in leaders_for_vertex:
        leader_for_vertex = leaders_for_vertex[vertex]
        leader_counter = scc_sizes.get(leader_for_vertex, 0) + 1
        scc_sizes[leader_for_vertex] = leader_counter

    scc_sizes_sorted = list(scc_sizes.values())
    scc_sizes_sorted.sort(reverse=True)

    return scc_sizes_sorted[:5]


def get_inverted_graph(graph_edges):
    """
    >>> get_inverted_graph([(2, 47646), (3, 4)])
    [(47646, 2), (4, 3)]

    :param graph_edges:
    :return:
    """
    inv_G = []

    for edge in graph_edges:
        inv_edge = edge[1], edge[0]
        inv_G.append(inv_edge)

    return inv_G


def get_adjacency_list(graph_edges):
    """
    >>> get_adjacency_list([(2, 47646), (2, 3), (3, 4)])
    {2: [47646, 3], 3: [4]}

    :param graph_edges:
    :return:
    """
    adjacency_dict = {}

    for edge in graph_edges:
        tail_vertex, head_vertex = edge
        vertex_adjacency_list = adjacency_dict.get(tail_vertex, [])
        vertex_adjacency_list.append(head_vertex)
        adjacency_dict[tail_vertex] = vertex_adjacency_list

    return adjacency_dict


def get_max_vertex_label(graph_adjacency_dict):
    """
    >>> get_max_vertex_label({2: [47646, 3], 3: [4]})
    3

    :param graph_adjacency_dict:
    :return:
    """
    lables = list(graph_adjacency_dict.keys())

    return max(lables)


def get_graph_edges_from_file(path):
    graph_edges = []

    with open(path, 'r') as raw_input_data:
        for line in raw_input_data:
            col = list(map(int, line.strip().split(' ')))
            # edges are directed from the first column vertex to the second column vertex
            tail_vertex = col[0]
            head_vertex = col[1]
            edge = tail_vertex, head_vertex
            graph_edges.append(edge)

    return graph_edges

if __name__ == '__main__':
    import doctest
    import sys

    print('recursionlimit: ', sys.getrecursionlimit())
    sys.setrecursionlimit(110000)

    doctest.testmod()

    path = 'SCC.txt'
    course_graph = get_graph_edges_from_file(path)
    course_graph_scc = get_scc(course_graph)
    print(course_graph_scc)