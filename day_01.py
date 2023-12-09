from aocutil import read, output, submit
data = read(__file__).splitlines()

# all representations of digits
digit_representations = {
    "0": 0, "zero": 0,
    "1": 1, "one": 1,
    "2": 2, "two": 2,
    "3": 3, "three": 3,
    "4": 4, "four": 4,
    "5": 5, "five": 5,
    "6": 6, "six": 6,
    "7": 7, "seven": 7,
    "8": 8, "eight": 8,
    "9": 9, "nine": 9
}

# so every digit really is in the string that we're indexing over later
all_digits_in_string = "".join(digit_representations.keys())

# sums for answer 1 and 2
answer_1 = answer_2 = 0

# for each line in the input string
for line in data:

    # for each digit representation, find its first occurrence, and record the digit corresponding to it
    positions = [(line + all_digits_in_string).index(x) for x in digit_representations]
    first_digit = (list(digit_representations.values())[positions.index(min(positions))])

    # also, do the line backwards, and find the occurrence of the backwards representation of the digit
    positions = [(all_digits_in_string + line)[::-1].index(x[::-1]) for x in digit_representations]
    last_digit = (list(digit_representations.values())[positions.index(min(positions))])

    # add this to the total for answer 2
    answer_2 += 10 * first_digit + last_digit

    # this is easier because we're only doing the single-digit representations
    digits_in_line = [int(i) for i in line if i.isnumeric()] 

    # directly gets out the first and last digits as numbers
    answer_1 += 10 * digits_in_line[0] + digits_in_line[-1]

# outputs the answers
output(answer_1)
output(answer_2)
