# -*- coding: utf-8 -*-


def merge_and_count_split_inv(B, C):
    """
    >>> merge_and_count_split_inv([1, 3, 5], [2, 4, 6])
    ([1, 2, 3, 4, 5, 6], 3)

    >>> merge_and_count_split_inv([1, 3, 5], [2, 4, 6, 7])
    ([1, 2, 3, 4, 5, 6, 7], 3)

    >>> merge_and_count_split_inv([1, 3, 5, 6], [2, 4, 7])
    ([1, 2, 3, 4, 5, 6, 7], 5)

    >>> merge_and_count_split_inv([1], [2])
    ([1, 2], 0)

    >>> merge_and_count_split_inv([2], [1])
    ([1, 2], 1)

    :param B:
    :param C:
    :return:
    """
    merged = []
    inv_counter = 0
    item_b = None
    item_c = None

    while (B or C or item_b or item_c):
        if not item_b and B:
            item_b = B.pop(0)

        if not item_c and C:
            item_c = C.pop(0)

        if item_b and item_c:
            if item_b <= item_c:
                merged.append(item_b)
                item_b = None
            else:
                merged.append(item_c)
                if item_b:
                    inv_counter += 1 + len(B)

                item_c = None
        else:
            if item_b:
                merged.append(item_b)
                item_b = None
            if item_c:
                merged.append(item_c)
                item_c = None

    return merged, inv_counter

def sort_and_count_array(A):
    """

    >>> sort_and_count_array([1, 2, 3, 4, 5, 6])
    ([1, 2, 3, 4, 5, 6], 0)
    >>> sort_and_count_array([1, 3, 5, 2, 4, 6])
    ([1, 2, 3, 4, 5, 6], 3)
    >>> sort_and_count_array([6, 5, 4, 3, 2, 1])
    ([1, 2, 3, 4, 5, 6], 15)
    """
    if len(A) == 1:
        return A, 0
    else:
        half_len = int(len(A) / 2)
        left_A = A[0:half_len]
        B, x = sort_and_count_array(left_A)
        right_A = A[half_len:]
        C, y = sort_and_count_array(right_A)
        D, z = merge_and_count_split_inv(B, C)
        return D, x + y + z


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    with open('input.txt', 'r') as raw_array:
        input_array = [int(line) for line in raw_array]

    result = sort_and_count_array(input_array)
    print(result[1])
