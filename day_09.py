from aocutil import read, output, submit
data = read(__file__).splitlines()
import numpy as np

# for a sequence, we want to get the next term by analysing common differences
def get_next_term(seq: list[int]):

    # differences should store the sequence, then the first differences, then the second, etc. down to when they're all zeroes
    differences = [np.array(seq)]

    # while the nth differences are not all zero, add them in order to the list
    while any(difference := (- differences[-1][:-1] + np.roll(differences[-1], -1)[:-1])):
        differences.append(difference)

    # now, differences is going to contain just integers, and be in the opposite order
    differences.append(0)
    differences = differences[::-1]

    # for each level of differences, take the next projected nth difference
    for i, schematic in enumerate(differences[1:], 1):
        differences[i] = schematic[-1] + differences[i-1]

    # the next projected 0th difference is just the next term in the sequence
    return differences[-1]

# the forwards sum is the sum of these, and the backwards sum is just what you get if you reverse each sequence and predict 
output(sum((get_next_term(list(map(int, line.split())))       for line in data)))
output(sum((get_next_term(list(map(int, line.split()))[::-1]) for line in data)))
    