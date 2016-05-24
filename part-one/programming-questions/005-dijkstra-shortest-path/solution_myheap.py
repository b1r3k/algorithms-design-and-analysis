# -*- coding: utf-8 -*-

import operator
import my_min_heap


def print_err(*args):
    print(*args, file=sys.stderr)


def get_node_idx(heap, node):
    for idx, item in enumerate(heap):
        dist, n = item
        if n == node:
            return idx

    return -1


def dijkstra_heapbased(source_node, graph_adjacency_list):
    """
    >>> dijkstra_heapbased(1, {1: [(2, 1), (3, 4)], 2: [(3, 2), (4, 6)], 3: [(1, 4), (2, 2), (4, 3)], 4: [(2, 6), (3, 3)]})
    {1: 0, 2: 1, 3: 3, 4: 6}

    >>> dijkstra_heapbased(1, {1: [(2, 1), (3, 4), (5, 0.5)], 2: [(3, 2), (4, 6)], 3: [(1, 4), (2, 2), (4, 3)], 4: [(2, 6), (3, 3)], 5: [(1, 0.5)]})
    {1: 0, 2: 1, 3: 3, 4: 6, 5: 0.5}

    :param source_node:
    :param graph_adjacency_list:
    :return:
    """
    heap = []
    shortest_distances = {}
    explored = []

    for node in graph_adjacency_list.keys():
        if node == source_node:
            my_min_heap.heappush(heap, (0, node))
        else:
            my_min_heap.heappush(heap, (float('inf'), node))

    while len(heap):
        current_distance, current_node = my_min_heap.heappop(heap)

        shortest_distances[current_node] = current_distance
        explored.append(current_node)

        # udpate heap
        adjacent_nodes = graph_adjacency_list.get(current_node, [])
        unexplored_nodes = list(filter(lambda adjacent_node: not operator.contains(explored, adjacent_node[0]), adjacent_nodes))

        for adjacent_node, adjacent_node_dist in unexplored_nodes:
            possible_dist = current_distance + adjacent_node_dist
            node_idx_in_heap = get_node_idx(heap, adjacent_node)

            # do we need to update this particular node?
            if node_idx_in_heap >= 0:
                node_dist = heap[node_idx_in_heap][0]
                if possible_dist < node_dist:
                    my_min_heap.remove(heap, node_idx_in_heap)
                else:
                    continue

            my_min_heap.heappush(heap, (possible_dist, adjacent_node))

    return shortest_distances


if __name__ == '__main__':
    import doctest
    import sys

    doctest.testmod()


