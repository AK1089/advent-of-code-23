from aocutil import read, output, submit
turn_sequence, nodes = read(__file__).split("\n\n")

from math import lcm

# turn sequence mapped as a set of booleans (False for L, True for R, so we can use them as indices)
turn_sequence = [t == "R" for t in turn_sequence]
node_map = {}

# for each line of the input main body, add the corresponding node to the map (the [1:-1] and [:-1] strip formatting)
for line in nodes.splitlines():
    raw_line_parts = line.split()
    node_map[raw_line_parts[0]] = (raw_line_parts[2][1:-1], raw_line_parts[3][:-1])

# the current cells we're in (ones ending with A), and which one of these represents "AAA"
current = [i for i in node_map if i.endswith("A")]
AAA_index, ZZZ_time = current.index("AAA"), 0

# how long it takes for each of the cells we're in to get to a cell ending with Z
# FLAWED ASSUMPTION: "the time it takes to get from ##A to ##Z is ALWAYS the same as the time it takes to then get back to ##Z again"
# this assumption was a deliberate risk  & turned out to be true, but did not have to be; this solution would not work without it!
times_to_absorption = [0 for _ in current]

# forever, keeping track of how many turns we're at
for i in range(1, 1000000000000000):

    # moves each ghost instance (takes the correct turn number), turns that into False/True for L/R, and uses that to move
    current = [node_map[c][turn_sequence[(i-1) % len(turn_sequence)]] for c in current]

    # if we've reached Z for the first time with a ghost instance, log the number of turns it's taken
    for j, raw_line_parts in enumerate(current):
        if raw_line_parts.endswith("Z") and not times_to_absorption[j]:
            times_to_absorption[j] = i

    # if we haven't yet hit ZZZ on the primary ghost instance, then do so
    if not ZZZ_time and current[AAA_index] == "ZZZ":
        ZZZ_time = i

    # if we've hit ##Z on all instances, then we're done!
    if 0 not in times_to_absorption:
        break

# this is the time to get to ZZZ on the primary, the next is how many it *would* take until all ##Zs line up
output(ZZZ_time)
output(lcm(*times_to_absorption))
