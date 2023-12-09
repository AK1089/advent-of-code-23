from aocutil import read, output, submit
data = read(__file__).split("\n\n")

# takes in the data: seed numbers are the first line, and the conversions are stored as lists of tuples of (destination, source, size)
seed_numbers, *raw_conversions_data = data
seed_numbers = list(map(int, seed_numbers.split()[1:]))
conversions = [[tuple(map(int, i.split())) for i in conversion.splitlines()[1:]] for conversion in raw_conversions_data]

# gets the final location number from a seed input
def get_location_from_seed_num(seed: int):

    # for each of the x-to-y maps, for each (destination, source, size) tuple within them
    for mapper in conversions:
        for shift in mapper:

            # if the seed is in the source range, move it the way it's supposed to be moved, and go to the next map
            if seed in range(shift[1], shift[1] + shift[2]):
                seed += shift[0] - shift[1]
                break
        
    # once every map has acted on it, it's been processed
    return seed

# answer to part 1: the minimal location number
output(min(map(get_location_from_seed_num, seed_numbers)))


# now, the seed numbers line means something different. 0, 2, 4... are starts and 1, 3, 5... are range lengths
seeds_start, seeds_len = seed_numbers[::2], seed_numbers[1::2]
seed_ranges = [range(a, a+b) for a,b in zip(seeds_start, seeds_len)]

# these are the numbers that are worthy of consideration - we can't try every single number!
# special numbers are those which are plausibly the lowest, as they *might* give a smaller result than their predecessor
# note that really these are "not non-special" numbers - nothing outside this list can be the answer, but most of the list is garbage
special_numbers = []

# now, let's backtrack through the set of maps
for mapper in conversions[::-1]:

    # these are the numbers that we're newly designating as special - separate lists so we don't modify while iterating
    special_numbers_workbook = []

    # for each shift, the start and just after the end of the ranges are plausibly special
    for shift in mapper:
        special_numbers_workbook.append(shift[1])
        special_numbers_workbook.append(shift[1] + shift[0])

        # also, for every number that's special later on, we need all numbers which map to it at this stage to be special
        for future_special_number in special_numbers:

            # so if it's in the destination range for this particular shift, the number which nontrivially maps to it is also special
            if future_special_number in range(shift[0], shift[0] + shift[2]):
                special_numbers_workbook.append(future_special_number + shift[1] - shift[0])

    # let's add all the new numbers to the overall special list
    special_numbers = list(set(special_numbers + special_numbers_workbook))

# filter this down to just numbers which are in our allowed ranges (by the first line of the input) and output the answer to part 2!
special_numbers = [i for i in special_numbers if any((i in x for x in seed_ranges))]
print(min(map(get_location_from_seed_num, special_numbers)))
