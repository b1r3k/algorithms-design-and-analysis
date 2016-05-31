# -*- coding: utf-8 -*-

import math


def get_parent_index(heap, children_index):
    """
    >>> get_parent_index([1, 2, 3], 1)
    0

    >>> get_parent_index([1, 2, 3, 4], 3)
    1

    >>> get_parent_index([1, 2, 3, 4], 0)
    0

    >>> get_parent_index([1, 2, 3], 0)
    0

    :param heap:
    :param children_index:
    :return:
    """

    if len(heap) % 2 == 0:
        parent_index = (children_index + 1) / 2
    else:
        parent_index = math.floor((children_index + 1) / 2)

    final_parent_idx = int(parent_index - 1)

    if final_parent_idx >= 0:
        return final_parent_idx

    return 0


def get_children_index(heap, parent_index):
    """
    >>> get_children_index([1, 2, 3], 0)
    1

    >>> get_children_index([4, 4, 8, 9, 4, 12, 9, 11, 13], 3)
    7

    >>> get_children_index([4, 4, 8, 9, 4, 12, 9, 11, 13], 2)
    5

    :param heap:
    :param parent_index:
    :return:
    """
    children_index = 2 * (parent_index + 1)

    return children_index - 1


def heappush(heap, item):
    """
    >>> heappush([4, 4, 8, 9, 4, 12, 9, 11, 13], 7)
    [4, 4, 8, 9, 4, 12, 9, 11, 13, 7]

    >>> heappush([4, 4, 8, 9, 4, 12, 9, 11, 13, 7], 10)
    [4, 4, 8, 9, 4, 12, 9, 11, 13, 7, 10]

    >>> heappush([4, 4, 8, 9, 4, 12, 9, 11, 13, 7, 10], 5)
    [4, 4, 5, 9, 4, 8, 9, 11, 13, 7, 10, 12]

    :param heap:
    :param item:
    :return:
    """
    heap.append(item)
    bubble_up(heap, len(heap) - 1)

    return heap


def heappop(heap):
    """
    bubble-down implements details for following operations

    >>> heappop([1])
    1

    >>> h = [4, 4, 8, 9, 4, 12, 9, 11, 13]
    >>> heappop(h)
    4

    >>> heappop(h)
    4

    >>> heappop(h)
    4

    >>> heappop(h)
    8

    :param heap:
    :return:
    """
    if len(heap) > 1:
        min_item = heap[0]
        heap[0] = heap.pop()
        bubble_down(heap, 0)
        return min_item
    else:
        return heap.pop(0)


def get_item_key(heap, item_index):
    try:
        return heap[item_index][0]
    except TypeError:
        return heap[item_index]


def remove(heap, item_index):
    """
    >>> remove([4, 4, 8, 9, 4, 12, 9, 11, 13], 3)
    [4, 4, 8, 11, 4, 12, 9, 13]

    >>> remove([4, 4, 8, 9, 4, 12, 9, 11, 13], 0)
    [4, 4, 8, 9, 13, 12, 9, 11]

    >>> remove([4, 4, 8, 9, 4, 12, 9, 11, 13], 8)
    [4, 4, 8, 9, 4, 12, 9, 11]

    >>> remove([4], 0)
    []

    >>> remove([4, 4, 8], 1)
    [4, 8]

    :param heap:
    :param item_index:
    :return:
    """

    if item_index == len(heap) - 1:
        heap.pop()
        return heap

    heap[item_index], heap[-1] = heap[-1], heap[item_index]
    heap.pop()
    keep_invariant(heap, get_parent_index(heap, item_index))
    children_index = get_children_index(heap, item_index)

    keep_invariant(heap, item_index)

    if children_index < len(heap) - 1:
        keep_invariant(heap, children_index)

    if children_index + 1 < len(heap) - 1:
        keep_invariant(heap, children_index + 1)

    return heap


def bubble_down(heap, item_index):
    """
    >>> bubble_down([13, 4, 8, 9, 4, 12, 9, 11], 0)
    [4, 4, 8, 9, 13, 12, 9, 11]

    >>> bubble_down([(13, 'a'), (4, 'b'), (8, 'c'), (9, 'd'), (4, 'e'), (12, 'f'), (9, 'g'), (11, 'h')], 0)
    [(4, 'b'), (4, 'e'), (8, 'c'), (9, 'd'), (13, 'a'), (12, 'f'), (9, 'g'), (11, 'h')]

    :param heap:
    :param item_index:
    :return:
    """

    children_index = get_children_index(heap, item_index)

    if children_index >= len(heap):
        return heap

    smallest_childs_index = list(filter(lambda idx: True if idx < len(heap) else False, [children_index, children_index + 1]))

    smallest_childs_index.sort(key=lambda idx: get_item_key(heap, idx))

    for child_idx in smallest_childs_index:
        if get_item_key(heap, item_index) > get_item_key(heap, child_idx):
            heap[item_index], heap[child_idx] = heap[child_idx], heap[item_index]
            return bubble_down(heap, child_idx)

    return heap


def bubble_up(heap, item_index):
    """
    >>> bubble_up([4, 4, 8, 9, 4, 12, 9, 11, 13, 7, 10, 5], 11)
    [4, 4, 5, 9, 4, 8, 9, 11, 13, 7, 10, 12]

    >>> bubble_up([4, 4, 8, 9, 4, 5], 5)
    [4, 4, 5, 9, 4, 8]

    >>> bubble_up([(4, 'a'), (4, 'b'), (8, 'c'), (9, 'd'), (4, 'e'), (5, 'new')], 5)
    [(4, 'a'), (4, 'b'), (5, 'new'), (9, 'd'), (4, 'e'), (8, 'c')]

    >>> bubble_up([5400, 5484, 5048], 2)
    [5048, 5484, 5400]

    :param heap:
    :param item_index:
    :return:
    """
    parent_index = get_parent_index(heap, item_index)
    parent_key = get_item_key(heap, parent_index)
    child_key = get_item_key(heap, item_index)

    if parent_key > child_key:
        heap[parent_index], heap[item_index] = heap[item_index], heap[parent_index]
        return bubble_up(heap, parent_index)

    return heap


def keep_invariant(heap, item_index):
    parent_index = get_parent_index(heap, item_index)

    if heap[parent_index] > heap[item_index]:
        return bubble_up(heap, item_index)
    else:
        return bubble_down(heap, item_index)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
