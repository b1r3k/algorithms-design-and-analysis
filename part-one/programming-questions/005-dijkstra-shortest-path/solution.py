# -*- coding: utf-8 -*-

import timeit

from solution_naive import dijkstra_naive
from solution_heapbased import dijkstra_heapbased


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


def get_significant_results(full_results, nodes_list):
    return map(lambda node: full_results.get(node, 1000000), nodes_list)


if __name__ == '__main__':
    path = 'dijkstraData.txt'
    number_executions = 1000
    course_graph = get_adjacency_list_from_file(path)

    t = timeit.Timer('dijkstra_naive(1, graph)', setup='from solution_naive import dijkstra_naive; from __main__ import get_adjacency_list_from_file; graph = get_adjacency_list_from_file("dijkstraData.txt")')
    print('Dijkstra naive implementation time performance: %s' % t.timeit(number_executions))
    naive_shortest_paths = dijkstra_naive(1, course_graph)

    naive_results = get_significant_results(naive_shortest_paths, [7, 37, 59, 82, 99, 115, 133, 165, 188, 197])
    print("Dijkstra naive implementation results: %s" % list(naive_results))

    t = timeit.Timer('dijkstra_heapbased(1, graph)', setup='from solution_heapbased import dijkstra_heapbased; from __main__ import get_adjacency_list_from_file; graph = get_adjacency_list_from_file("dijkstraData.txt")')
    print('Dijkstra heapbased implementation time performance: %s' % t.timeit(number_executions))

    heapbased_shortest_paths = dijkstra_heapbased(1, course_graph)

    heapbased_results = get_significant_results(heapbased_shortest_paths, [7, 37, 59, 82, 99, 115, 133, 165, 188, 197])
    print("Dijkstra heapbased implementation results: %s" % list(heapbased_results))
