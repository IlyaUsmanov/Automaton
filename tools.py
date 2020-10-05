from itertools import combinations, chain

def powerset(base_set):
    result = list()
    for len_of_subset in range(1, len(base_set) + 1):
        for subset in tuple(combinations(base_set, len_of_subset)):
            result.append(set(subset))
    return result

