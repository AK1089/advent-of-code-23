from aocutil import read, output, submit
data = read(__file__).splitlines()

# times and distances if they're four races, vs if they're just 1
times = list(map(int, data[0].split()[1:]))
distances = list(map(int, data[1].split()[1:]))
time_part_2 = int(data[0][9:].replace(" ", ""))
distance_part_2 = int(data[1][9:].replace(" ", ""))

# how many options there are for the first one
options_part_1 = 1

# for each of the four races in part 1, calculate the number of options
# this is done by rearranging and solving the quadratic, rather than looping!
for t, d in zip(times, distances):
    upper_solution = int(1/2 * (t + ((t**2 - 4 * d) ** 0.5)) - 0.000001)
    options_part_1 *= (upper_solution * 2 - t + 1)

# do the same but with the part 2 race
upper_solution = int(1/2 * (time_part_2 + ((time_part_2**2 - 4 * distance_part_2) ** 0.5)) - 0.000001)
options_part_2 = (upper_solution * 2 - time_part_2 + 1)

# output the answer
output(options_part_1)
output(options_part_2)
