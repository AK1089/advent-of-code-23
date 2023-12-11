from aocutil import read, output, submit
data = read(__file__).splitlines()

# convert into lists, including adding a line at the end
positions = [list(line) for line in data]
positions.append(list("." * len(positions[0])))

# the start position and current position (we start by going rightwards) as integer coordinates
current_position = "".join(data).index("S")
start_position = [current_position // len(positions[0]), current_position % len(positions[0])]
current_position = [start_position[0], start_position[1] + 1]

# on the first turn, we're going rightwards (and have moved one cell). the only cell in the path so far is the start cell
facing_direction = "right"
all_cells_on_path = [start_position]

# until we get back round to the start, keep adding cells to the path and traversing the loop
while current_position != start_position:
    all_cells_on_path.append(current_position.copy())

    # this is all possible ways to go into a cell and out, and what direction they would make you move
    facing_direction = {
        ("up", "F"):    "right",
        ("left", "F"):  "down",
        ("down", "J"):  "left",
        ("right", "J"): "up",
        ("left", "L"):  "up",
        ("down", "L"):  "right",
        ("right", "7"): "down",
        ("up", "7"):    "left",
        ("up", "|"):    "up",
        ("down", "|"):  "down",
        ("left", "-"):  "left",
        ("right", "-"): "right",
    }[(facing_direction, data[current_position[0]][current_position[1]])]

    # if you're facing in a certain direction, that's equivalent to changing your position in this way
    if facing_direction == "up":      current_position[0] -= 1
    elif facing_direction == "down":  current_position[0] += 1
    elif facing_direction == "left":  current_position[1] -= 1
    elif facing_direction == "right": current_position[1] += 1

    # progress one unit around the path
    assert current_position[0] not in (0, len(positions)-1) and current_position[1] not in (0, len(positions[0])-1)


# number of cells contained within the loop
number_of_cells_on_inside = 0

# for each row, we can track inside cells individually. status is 0 (even) to indicate "not inside the loop" as of the left edge
for y, row in enumerate(positions):
    vertical_thresholds_crossed = 0

    # for each cell in the row, from left to right:
    for x, cell in enumerate(row):

        # convert it into a nice-looking path that we can render: nice symbols if it's on the path, a blank space otherwise
        positions[y][x] = {"|": "┃", "-": "━", "L": "┗", "7": "┓", "J": "┛", "F": "┏", " ": " ", ".": ".", "S": "┏"}[positions[y][x]] if [y, x] in all_cells_on_path else " "

        # for cells that matter we're counting "vertical thresholds crossed": | counts for 1, ┏/┛are +1/2, ┗/┓are -1/2
        vertical_thresholds_crossed += {"┏": 1/2, "┛": 1/2, "┗": -1/2, "┓": -1/2, "┃": 1, "━": 0, " ": 0}[positions[y][x]]

        # for cells that aren't on the path if we've crossed an odd number of vertical thresholds, we're inside the loop - mark the cell
        if [y, x] not in all_cells_on_path and vertical_thresholds_crossed % 2:
            number_of_cells_on_inside += 1
            positions[y][x] = "."

# output the distance, which is half the length of the pipe, and the number of cells contained within the loop
output(len(all_cells_on_path) // 2)
output(number_of_cells_on_inside)
