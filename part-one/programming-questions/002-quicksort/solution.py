# -*- coding: utf-8 -*-

def get_first_pivot_idx(A, start_idx, stop_idx):
    return start_idx

def get_last_pivot_idx(A, start_idx, stop_idx):
    return stop_idx - 1


def get_median_pivot_idx(A, start_idx, stop_idx):
    """
    >>> get_median_pivot_idx([8, 2, 4, 5, 7, 1], 0, 6)
    2

    >>> get_median_pivot_idx([4, 5, 6, 7], 0, 4)
    1

    >>> get_median_pivot_idx([3, 8 ,2, 5, 1, 4, 7, 6], 3, 8)
    3

    >>> get_median_pivot_idx([1, 3, 5, 2, 4, 6], 3, 6)
    4

    :param A:
    :param start_idx:
    :param stop_idx:
    :return:
    """
    first_item = A[start_idx], start_idx
    last_item = A[stop_idx - 1], stop_idx - 1
    middle_item_idx = start_idx + int((stop_idx - start_idx - 1) / 2)
    middle_item = A[middle_item_idx], middle_item_idx

    items = [first_item, middle_item, last_item]
    items.sort(key=lambda k: k[0])

    return items[1][1]


def partition(A, start_idx, stop_idx, pivot_idx):
    """
    FIRST

    >>> partition([3, 8 ,2, 5, 1, 4, 7, 6], 0, 8, 0)
    2

    >>> partition([3, 8 ,2, 5, 1, 4, 7, 6], 3, 8, 3)
    5

    >>> partition([2, 1], 0, 2, 0)
    1

    LAST

    >>> partition([3, 4, 2, 1, 6], 0, 5, 4)
    4

    >>> partition([3, 4, 2, 1, 6], 2, 5, 4)
    4

    >>> partition([6, 3], 0, 2, 0)
    1

    MEDIAN

    >>> partition([3, 4, 2, 1, 6], 0, 5, 2)
    1

    >>> partition([3, 4, 2, 1, 6], 1, 5, 3)
    1

    >>> partition([688, 117, 468, 885, 64, 419, 374, 645, 716, 75], 0, 10, 0)
    7

    """

    A[start_idx], A[pivot_idx] = A[pivot_idx], A[start_idx]

    pivot = A[start_idx]
    initial_pivot_idx = start_idx
    final_pivot_idx = start_idx + 1

    for item_idx in range(start_idx, stop_idx):
        if A[item_idx] < pivot:
            A[final_pivot_idx], A[item_idx] = A[item_idx], A[final_pivot_idx]
            final_pivot_idx += 1

    A[initial_pivot_idx], A[final_pivot_idx - 1] = A[final_pivot_idx - 1], A[initial_pivot_idx]

    return final_pivot_idx - 1


def quicksort(A, **kwargs):
    """

    >>> quicksort([1, 2, 3, 4, 5, 6])[0]
    [1, 2, 3, 4, 5, 6]

    >>> quicksort([1, 3, 5, 2, 4, 6])[0]
    [1, 2, 3, 4, 5, 6]

    >>> quicksort([6, 5, 4, 3, 2, 1])[0]
    [1, 2, 3, 4, 5, 6]

    >>> quicksort([6, 5, 4, 3, 2, 1, 1])[0]
    [1, 1, 2, 3, 4, 5, 6]

    >>> quicksort([6, 6, 5, 4, 3, 2, 1])[0]
    [1, 2, 3, 4, 5, 6, 6]

    >>> quicksort([6, 5, 4, 3, 2, 1, 43])[0]
    [1, 2, 3, 4, 5, 6, 43]

    >>> quicksort([688, 117, 468, 885, 64, 419, 374, 645, 716, 75])[0]
    [64, 75, 117, 374, 419, 468, 645, 688, 716, 885]

    >>> quicksort([3, 2, 1, 4])[1]
    4

    >>> quicksort([1, 2, 3, 4])[1]
    6

    >>> quicksort([1, 2, 3, 4], pivoting_func=get_last_pivot_idx)[1]
    6

    >>> quicksort([688, 117, 468, 885, 64, 419, 374, 645, 716, 75])[1]
    22

    """

    start_idx = kwargs.get('start_idx', 0)
    stop_idx = kwargs.get('stop_idx', len(A))
    pivoting_func = kwargs.get('pivoting_func', get_first_pivot_idx)

    if start_idx is None:
        start_idx = 0

    if stop_idx is None:
        stop_idx = len(A)

    slice_len = stop_idx - start_idx

    if slice_len < 2:
        return [], 0

    no_cmps = slice_len - 1

    pivot_idx = pivoting_func(A, start_idx, stop_idx)
    pivot_idx = partition(A, start_idx, stop_idx, pivot_idx)
    left_result = quicksort(A, start_idx=start_idx, stop_idx=pivot_idx, pivoting_func=pivoting_func)
    right_result = quicksort(A, start_idx=pivot_idx + 1, stop_idx=stop_idx, pivoting_func=pivoting_func)

    no_cmps += left_result[1]
    no_cmps += right_result[1]

    return A, no_cmps


if __name__ == '__main__':
    import doctest
    import sys

    print('recursionlimit: ', sys.getrecursionlimit())
    sys.setrecursionlimit(11000)

    doctest.testmod()

    with open('input.txt', 'r') as raw_array:
        input_array = [int(line) for line in raw_array]

        A = input_array.copy()
        B = input_array.copy()
        C = input_array.copy()

        result = quicksort(A, pivoting_func=get_first_pivot_idx)
        print('No of comparisons (first element as pivot):', result[1]) # correct: 162085 comparisons

        result = quicksort(B, pivoting_func=get_last_pivot_idx)
        print('No of comparisons (last element as pivot):', result[1]) # correct: 164123 comparisons

        result = quicksort(C, pivoting_func=get_median_pivot_idx)
        print('No of comparisons (median element as pivot):', result[1]) # correct: 138382 comparisons
