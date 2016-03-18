# -*- coding: utf-8 -*-

import sys
import copy
import operator


def print_err(*args):
    print(*args, file=sys.stderr)


def get_closest_node(graph, explored, shortest_distances):
    shortest_paths = []

    for explored_node in explored:
        explored_node_dist = shortest_distances[explored_node]
        adjacent_nodes = graph.get(explored_node, [])
        unexplored_nodes = list(filter(lambda adjacent_node: not operator.contains(explored, adjacent_node[0]), adjacent_nodes))
        possible_paths_lengths = list(map(lambda adjacent_node: (adjacent_node[0], explored_node_dist + adjacent_node[1]), unexplored_nodes))
        sorted_paths_lengths = sorted(possible_paths_lengths, key=lambda adjacent_node_tuple: adjacent_node_tuple[1])
        if len(sorted_paths_lengths):
            shortest_paths.append(sorted_paths_lengths[0])

    shortest_paths.sort(key=lambda adjacent_node_tuple: adjacent_node_tuple[1])

    if len(shortest_paths):
        return shortest_paths[0]
    else:
        return None, None


def dijkstra_naive(source_node, graph_adjacency_list):
    """
    >>> dijkstra_naive(1, {1: [(2, 1), (3, 4)], 2: [(3, 2), (4, 6)], 3: [(1, 4), (2, 2), (4, 3)], 4: [(2, 6), (3, 3)]})
    {1: 0, 2: 1, 3: 3, 4: 6}

    >>> dijkstra_naive(1, {1: [(2, 1), (3, 4), (5, 0.5)], 2: [(3, 2), (4, 6)], 3: [(1, 4), (2, 2), (4, 3)], 4: [(2, 6), (3, 3)], 5: [(1, 0.5)]})
    {1: 0, 2: 1, 3: 3, 4: 6, 5: 0.5}

    :param source_node:
    :param graph_adjacency_list:
    :return:
    """
    shortest_distances = {source_node: 0}

    nodes_pool = set(graph_adjacency_list.keys()) - set([source_node])
    explored = [source_node]

    while len(nodes_pool):
        current_node, current_distance = get_closest_node(graph_adjacency_list, explored, shortest_distances)

        if current_node:
            shortest_distances[current_node] = current_distance
            explored.append(current_node)
            nodes_pool.remove(current_node)

    return shortest_distances


def get_adjacency_list_from_file(path):
    graph = {}

    with open(path, 'r') as raw_input_data:
        for line in raw_input_data:
            col = list(line.strip().split('\t'))
            # example row
            # 6	141,8200	98,5594	66,6627	159,9500
            # vertex TAB adjacent_vertex,length TAB adjacent_vertex,length
            vertex = int(col[0])
            vertex_adjacency_list = []
            for vertex_length_tuple in col[1:]:
                adjacent_vertex, length = map(int, vertex_length_tuple.split(','))
                vertex_adjacency_list.append((adjacent_vertex, length))

            graph[vertex] = vertex_adjacency_list

    return graph


if __name__ == '__main__':
    import doctest
    import sys

    doctest.testmod()

    path = 'dijkstraData.txt'
    course_graph = get_adjacency_list_from_file(path)
    final_shortest_paths = dijkstra_naive(1, course_graph)
    results = map(lambda node: final_shortest_paths.get(node, 1000000), [7, 37, 59, 82, 99, 115, 133, 165, 188, 197])
    print(list(results))

