# -*- coding: utf-8 -*-


import operator


def print_err(*args):
    print(*args, file=sys.stderr)


def get_closest_node(graph, explored, shortest_distances):
    shortest_paths = []

    for explored_node in explored:
        explored_node_dist = shortest_distances[explored_node]
        adjacent_nodes = graph.get(explored_node, [])
        unexplored_nodes = list(filter(lambda adjacent_node: not operator.contains(explored, adjacent_node[0]), adjacent_nodes))
        if unexplored_nodes:
            possible_paths_lengths = list(map(lambda adjacent_node: (adjacent_node[0], explored_node_dist + adjacent_node[1]), unexplored_nodes))
            min_path_node = min(possible_paths_lengths, key=lambda adjacent_node_tuple: adjacent_node_tuple[1])
            shortest_paths.append(min_path_node)

    if len(shortest_paths):
        return min(shortest_paths, key=lambda adjacent_node_tuple: adjacent_node_tuple[1])
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


if __name__ == '__main__':
    import doctest
    import sys

    doctest.testmod()



