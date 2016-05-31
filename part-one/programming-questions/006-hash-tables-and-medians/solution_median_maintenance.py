# -*- coding: utf-8 -*-

import timeit
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent) + '/' + '005-dijkstra-shortest-path')

import my_max_heap
import my_min_heap

def get_input(path):
    array = []

    with open(path, 'r') as raw_input_data:
        for line in raw_input_data:
            num = int(line.strip())
            array.append(num)

    return array


def rebalance_heaps(heap_low, heap_high):
    rebalanced_heap_low = heap_low
    rebalanced_heap_high = heap_high

    if len(rebalanced_heap_low) - len(rebalanced_heap_high) > 1:
        element = my_max_heap.heappop(rebalanced_heap_low)
        my_min_heap.heappush(rebalanced_heap_high, element)

    if len(rebalanced_heap_high) - len(rebalanced_heap_low) > 1:
        element = my_min_heap.heappop(rebalanced_heap_high)
        my_max_heap.heappush(rebalanced_heap_low, element)

    return rebalanced_heap_low, rebalanced_heap_high


def insert(heap_low, heap_high, num):
    hl = heap_low.copy()
    hh = heap_high.copy()

    if len(hl) == 0 or num < hl[0]:
        my_max_heap.heappush(hl, num)
    else:
        my_min_heap.heappush(hh, num)

    return hl, hh


def solution(array):
    """
    # >>> solution([5, -5, 6, -6])
    # [5, -5, 5, -5]

    # >>> solution([41558, 32184, -54788, 8684, -90716, -25835, -77485, -25580, 54844, 35411])
    # [41558, 32184, 32184, 8684, 8684, -25835, -25835, -25835, -25580, -25580]

    >>> solution([5400, 2138, 1344, 5484, 5048, 4338, 5078, 7733, 1692, 9052, 1779, 8086, 8299, 6601, 1115, 735, 3031, 978, 880, 2132])
    [5400, 2138, 2138, 2138, 5048, 4338, 5048, 5048, 5048, 5048, 5048, 5048, 5078, 5078, 5078, 5048, 5048, 4338, 4338, 3031]

    """
    heap_low = [] # extract-max
    heap_high = [] # extract-min
    median_list = []

    for num in array:
        heap_low, heap_high = insert(heap_low, heap_high, num)
        heap_low, heap_high = rebalance_heaps(heap_low, heap_high)

        if len(heap_low) == len(heap_high):
            median = heap_low[0]
        else:
            if len(heap_low) > len(heap_high):
                median = heap_low[0]
            else:
                median = heap_high[0]

        median_list.append(median)
        # print(median_list)

    return median_list

if __name__ == '__main__':
    import doctest

    doctest.testmod()

    array = get_input('./Median.txt')
    medians = solution(array)
    print('%d' % (sum(medians) % 10000))

