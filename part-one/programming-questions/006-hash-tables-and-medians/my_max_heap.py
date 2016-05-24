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
    # we should get max at heap[0]
    >>> heap = []
    >>> heap = heappush(heap, 1)
    >>> heap = heappush(heap, 3)
    >>> heap = heappush(heap, 4)
    >>> heap = heappush(heap, 16)
    >>> heap[0]
    16

    >>> heappush([4, 4, 8, 9, 4, 12, 9, 11, 13], 7)
    [7, 4, 8, 9, 4, 12, 9, 11, 13, 4]

    >>> heappush([7, 4, 8, 9, 4, 12, 9, 11, 13, 4], 10)
    [10, 7, 8, 9, 4, 12, 9, 11, 13, 4, 4]

    >>> heappush([10, 7, 8, 9, 4, 12, 9, 11, 13, 4, 4], 13)
    [13, 7, 10, 9, 4, 8, 9, 11, 13, 4, 4, 12]

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

    >>> h = [13, 6, 5, 4, 8]
    >>> heappop(h)
    13

    >>> heappop(h)
    8

    >>> heappop(h)
    6

    :param heap:
    :return:
    """
    if len(heap) > 1:
        max_item = heap[0]
        heap[0] = heap.pop()
        bubble_down(heap, 0)
        return max_item
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
    [13, 4, 8, 4, 4, 12, 9, 11]

    >>> remove([4, 4, 8, 9, 4, 12, 9, 11, 13], 0)
    [13, 9, 12, 11, 4, 8, 9, 4]

    >>> remove([4, 4, 8, 9, 4, 12, 9, 11, 13], 8)
    [4, 4, 8, 9, 4, 12, 9, 11]

    >>> remove([4], 0)
    []

    >>> remove([4, 4, 8], 1)
    [8, 4]

    :param heap:
    :param item_index:
    :return:
    """

    if item_index == len(heap) - 1:
        heap.pop()
        return heap

    heap[item_index], heap[-1] = heap[-1], heap[item_index]
    heap.pop()
    # keep_invariant(heap, get_parent_index(heap, item_index))
    children_index = get_children_index(heap, item_index)

    keep_invariant(heap, item_index)

    if children_index < len(heap) - 1:
        keep_invariant(heap, children_index)

    if children_index + 1 < len(heap) - 1:
        keep_invariant(heap, children_index + 1)

    return heap


def bubble_down(heap, item_index):
    """
    >>> bubble_down([4, 5, 6], 0)
    [6, 5, 4]

    # exchange 3 with 10
    >>> bubble_down([4, 1, 3, 2, 16, 9, 10, 14, 8, 7], 2)
    [4, 1, 10, 2, 16, 9, 3, 14, 8, 7]


    :param heap:
    :param item_index:
    :return:
    """

    children_index = get_children_index(heap, item_index)

    if children_index >= len(heap):
        return heap

    smallest_childs_index = list(filter(lambda idx: True if idx < len(heap) else False, [children_index, children_index + 1]))

    smallest_childs_index.sort(key=lambda idx: get_item_key(heap, idx), reverse=True)

    for child_idx in smallest_childs_index:
        if get_item_key(heap, item_index) < get_item_key(heap, child_idx):
            heap[item_index], heap[child_idx] = heap[child_idx], heap[item_index]
            return bubble_down(heap, child_idx)

    return heap


def bubble_up(heap, item_index):
    """
    >>> bubble_up([4, 4, 8, 9, 4, 12, 9, 11, 13, 7, 10, 5], 8)
    [13, 4, 8, 4, 4, 12, 9, 11, 9, 7, 10, 5]

    >>> bubble_up([4, 4, 8, 9, 4, 5], 3)
    [9, 4, 8, 4, 4, 5]

    >>> bubble_up([7, 4, 8, 9, 4, 12, 9, 11, 13, 4, 10], 10)
    [10, 7, 8, 9, 4, 12, 9, 11, 13, 4, 4]


    :param heap:
    :param item_index:
    :return:
    """
    parent_index = get_parent_index(heap, item_index)
    parent_key = get_item_key(heap, parent_index)
    child_key = get_item_key(heap, item_index)

    if parent_key < child_key:
        heap[parent_index], heap[item_index] = heap[item_index], heap[parent_index]
        return bubble_up(heap, parent_index)

    return heap


def keep_invariant(heap, item_index):
    parent_index = get_parent_index(heap, item_index)

    if heap[parent_index] < heap[item_index]:
        return bubble_up(heap, item_index)
    else:
        return bubble_down(heap, item_index)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
