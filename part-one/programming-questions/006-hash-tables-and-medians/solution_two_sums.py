# -*- coding: utf-8 -*-


def get_input(path):
    array = []

    with open(path, 'r') as raw_input_data:
        for line in raw_input_data:
            num = int(line.strip())
            array.append(num)

    return array


def has_two_sum(hash_table, two_sum):
    for integer in hash_table:
        complementary_int = two_sum - integer
        if hash_table.get(complementary_int, False):
            return True

    return False


def solution(uniq_integers, min_range = -10000, max_range=10000):
    """
    >>> solution([10000, -10000])
    1

    >>> solution([5000, 5000])
    1

    >>> solution([1, -1, 3, -3, 3], -1, 1)
    1

    >>> solution([1, -1, 3, -3, 3], -3, 3)
    3

    """
    sums_counter = 0
    hash_table = {}

    uniq_integers.sort()

    for integer in uniq_integers:
        hash_table[integer] = True

    for two_sum in range(min_range, max_range + 1):
        if has_two_sum(hash_table, two_sum):
            sums_counter += 1

    return sums_counter


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    integers = get_input('algo1_programming_prob_2sum.txt')
    uniq_integers = list(set(integers))
    no_sums = solution(uniq_integers)
    print(no_sums)



