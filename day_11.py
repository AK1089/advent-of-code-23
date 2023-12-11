from aocutil import read, output, submit
data = read(__file__).splitlines()

# which rows/columns are empty space and need to be extended? where are the galaxies?
rows_extended, cols_extended = [], []
galaxy_locations = []

# for each row, add its index to the list of empty rows if there are no galaxies
for i,x in enumerate(data):
    if "#" not in x:
        rows_extended.append(i)

# transpose the data
data = list(zip(*data))

# for each "row" (originally a column), add its index to the list of empty columns if there are no galaxies
for i,x in enumerate(data):
    if "#" not in x:
        cols_extended.append(i)

# re-transpose the data to its original orientation
data = list(zip(*data))

# locate all the galaxies
for y, row in enumerate(data):
    for x, cell in enumerate(row):
        if cell == "#":
            galaxy_locations.append([y, x])

# to store our answers
part_1_answer = part_2_answer = 0

# for each ordered pair of galaxies
for a in galaxy_locations:
    for b in galaxy_locations:

        # Euclidean distance between them on the original map, plus the extra distance for each expanded row/col you cross
        part_1_answer += abs(a[0] - b[0]) + abs(a[1] - b[1]) + (
            (len([i for i in rows_extended if i in range(min(a[0], b[0]), max(a[0], b[0]))])) + 
            (len([j for j in cols_extended if j in range(min(a[1], b[1]), max(a[1], b[1]))]))
            )

        # for part 2, the extra distance is 999,999 rather than just 1 for each expanded row/column
        part_2_answer += abs(a[0] - b[0]) + abs(a[1] - b[1]) + (
            999999*(len([i for i in rows_extended if i in range(min(a[0], b[0]), max(a[0], b[0]))])) + 
            999999*(len([j for j in cols_extended if j in range(min(a[1], b[1]), max(a[1], b[1]))]))
            )

# output the answers, though they need to be halved because we've double counted each galaxy pair
output(part_1_answer // 2)
output(part_2_answer // 2)
