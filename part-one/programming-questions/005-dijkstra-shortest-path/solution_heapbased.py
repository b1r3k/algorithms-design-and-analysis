# -*- coding: utf-8 -*-

import operator
import heapq


def print_err(*args):
    print(*args, file=sys.stderr)


def get_node_idx(heap, node):
    for idx, item in enumerate(heap):
        dist, n = item
        if n == node:
            return idx

    return -1


def delete_item(heap, item_idx):
    del heap[item_idx]
    heap.sort()
    return True


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
            heapq.heappush(heap, (0, node))
        else:
            heapq.heappush(heap, (float('inf'), node))

    while len(heap):
        current_distance, current_node = heapq.heappop(heap)

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
                    delete_item(heap, node_idx_in_heap)
                else:
                    continue

            heapq.heappush(heap, (possible_dist, adjacent_node))

    return shortest_distances




def solve():
    path = 'dijkstraData.txt'
    course_graph = get_adjacency_list_from_file(path)
    heapbased_shortest_paths = dijkstra_heapbased(1, course_graph)

    heapbased_results = get_significant_results(heapbased_shortest_paths, [7, 37, 59, 82, 99, 115, 133, 165, 188, 197])
    print(list(heapbased_results))


if __name__ == '__main__':
    import doctest
    import sys

    doctest.testmod()


