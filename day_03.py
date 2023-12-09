from aocutil import read, output, submit
data = read(__file__).splitlines()

# the size of the grid as (height, width)
SIZE = (len(data), len(data[0]))

# the grid of symbols in the input, grid of booleans for whether a spot is next to a symbol, and grid of integer gear numbers
grid_of_symbols = [list("." * (SIZE[1] + 2))]
grid_next_to_symbol = []
grid_gear_numbers = []

# grid of symbols should be the data padded on all four sides with dots
for i, line in enumerate(data):
    grid_of_symbols.append(list(f".{line}."))
grid_of_symbols.append(list("." * (SIZE[1] + 2)))

# copy this size into the other two lists with default values
for line in grid_of_symbols:
    grid_next_to_symbol.append([False for _ in line])
    grid_gear_numbers.append([0 for _ in line])


# we need to store which gear numbers haven't yet been used, and which ones are special (have two numbers on the same line)
current_unused_gear_num = 0
special_gear_numbers = []


# part of answer to Part 1: for each cell in the grid, check that it's not a number or a blank spot
for y, row in enumerate(grid_of_symbols):
    for x, cell in enumerate(row):
        if not cell.isnumeric() and cell != ".":

            # flag the spot and all adjacent spots as being "next to a symbol"
            grid_next_to_symbol[y+1][x+1] = True
            grid_next_to_symbol[y][x+1]   = True
            grid_next_to_symbol[y-1][x+1] = True
            grid_next_to_symbol[y+1][x]   = True
            grid_next_to_symbol[y][x]     = True
            grid_next_to_symbol[y-1][x]   = True
            grid_next_to_symbol[y+1][x-1] = True
            grid_next_to_symbol[y][x-1]   = True
            grid_next_to_symbol[y-1][x-1] = True


# for each cell in the symbol grid
for y, row in enumerate(grid_of_symbols):
    for x, cell in enumerate(row):

        # if it's a gear, then we're looking for nearby numbers to make part numbers
        if cell == "*":

            # this is 1 for each adjacent number on the same row
            partnum = grid_of_symbols[y][x+1].isnumeric() + grid_of_symbols[y][x-1].isnumeric()

            # this is: 0 for ... | 1 for 9.. / .9. / ..9 / 99. / .99 / 999 | 2 for 9.9 [on the row above]
            partnum += (grid_of_symbols[y-1][x-1].isnumeric() + grid_of_symbols[y-1][x].isnumeric() + grid_of_symbols[y-1][x+1].isnumeric())
            partnum -= (grid_of_symbols[y-1][x-1].isnumeric() and grid_of_symbols[y-1][x].isnumeric())
            partnum -= (grid_of_symbols[y-1][x].isnumeric() and grid_of_symbols[y-1][x+1].isnumeric())

            # this is: 0 for ... | 1 for 9.. / .9. / ..9 / 99. / .99 / 999 | 2 for 9.9 [on the row below]
            partnum += (grid_of_symbols[y+1][x-1].isnumeric() + grid_of_symbols[y+1][x].isnumeric() + grid_of_symbols[y+1][x+1].isnumeric())
            partnum -= (grid_of_symbols[y+1][x-1].isnumeric() and grid_of_symbols[y+1][x].isnumeric())
            partnum -= (grid_of_symbols[y+1][x].isnumeric() and grid_of_symbols[y+1][x+1].isnumeric())

            # we only care about the gears with part number 2 - let's pick a new gear number for it
            if partnum == 2:
                current_unused_gear_num += 1

                # the gear is special if it's got numbers on both sides of it on its own row
                if grid_of_symbols[y][x+1].isnumeric() and grid_of_symbols[y][x-1].isnumeric():
                     special_gear_numbers.append(current_unused_gear_num)

                # it's also special if it follows the 9.9 pattern on the row above or below
                if (grid_of_symbols[y-1][x-1].isnumeric() and not grid_of_symbols[y-1][x].isnumeric() and grid_of_symbols[y-1][x+1].isnumeric()):
                     special_gear_numbers.append(current_unused_gear_num)
                if (grid_of_symbols[y+1][x-1].isnumeric() and not grid_of_symbols[y+1][x].isnumeric() and grid_of_symbols[y+1][x+1].isnumeric()):
                     special_gear_numbers.append(current_unused_gear_num)

                # for all 8 adjacent cells, if they're numbers, set their gear numbers in the table to this gear's number
                grid_gear_numbers[y+1][x+1] = grid_of_symbols[y+1][x+1].isnumeric() * current_unused_gear_num
                grid_gear_numbers[y][x+1]   = grid_of_symbols[y][x+1].isnumeric()   * current_unused_gear_num
                grid_gear_numbers[y-1][x+1] = grid_of_symbols[y-1][x+1].isnumeric() * current_unused_gear_num
                grid_gear_numbers[y+1][x]   = grid_of_symbols[y+1][x].isnumeric()   * current_unused_gear_num
                grid_gear_numbers[y-1][x]   = grid_of_symbols[y-1][x].isnumeric()   * current_unused_gear_num
                grid_gear_numbers[y+1][x-1] = grid_of_symbols[y+1][x-1].isnumeric() * current_unused_gear_num
                grid_gear_numbers[y][x-1]   = grid_of_symbols[y][x-1].isnumeric()   * current_unused_gear_num
                grid_gear_numbers[y-1][x-1] = grid_of_symbols[y-1][x-1].isnumeric() * current_unused_gear_num


# expand the scope of all numbers flagged as being next to a symbol - no number is >4 long
for _ in range(5):

    # for each cell in the grid, if it's a number
    for y, row in enumerate(grid_of_symbols):
        for x, cell in enumerate(row):
            if cell.isnumeric():

                # if the left or right cell is a number and part of a gear ratio, then this cell inherits its gear ratio
                if ((grid_of_symbols[y][x-1].isnumeric() and grid_gear_numbers[y][x-1]) or (grid_of_symbols[y][x+1].isnumeric() and grid_gear_numbers[y][x+1])):
                    grid_gear_numbers[y][x] = max((grid_gear_numbers[y][x-1], grid_gear_numbers[y][x+1]))

                # similarly, if an adjacent cell is next to a symbol then this one is too (indirectly)
                if ((grid_of_symbols[y][x-1].isnumeric() and grid_next_to_symbol[y][x-1]) or (grid_of_symbols[y][x+1].isnumeric() and grid_next_to_symbol[y][x+1])):
                    grid_next_to_symbol[y][x] = True


# to store the answers
answer_part_1 = answer_part_2 = 0


# for each symbol, wipe it to . unless it's specifically a number which is next to a symbol
for y, row in enumerate(grid_of_symbols):
    for x, cell in enumerate(row):
        grid_of_symbols[y][x] = grid_of_symbols[y][x] if grid_next_to_symbol[y][x] and grid_of_symbols[y][x].isnumeric() else "."

    # take the row, read it as a string, split the numbers by dots, and add the sum (blank spaces between dots are zero)
    answer_part_1 += (sum([int(number or 0) for number in "".join(grid_of_symbols[y]).split(".")]))


# for each grid number, wipe it to . unless it's specifically a number which is part of a gear ratio (subset of previous condition)
for y, row in enumerate(grid_gear_numbers):
    for x, cell in enumerate(row):
        grid_of_symbols[y][x] = grid_of_symbols[y][x] if cell and grid_of_symbols[y][x].isnumeric() else "."

# for all the gears we have, create a dictionary that maps a gear id to its two part numbers
ratios_to_numbers = {x:[] for x in range(0, current_unused_gear_num + 1)}

# for each row in the new symbol grid, we want to put its numbers in the correct gear bucket
for y, row in enumerate(grid_of_symbols):
    set_of_used_ratios_this_line = []

    # add each nonzero gear number in the corresponding row to the list at most once (twice if it's a special gear)
    for x in grid_gear_numbers[y]:
        if x !=  0 and set_of_used_ratios_this_line.count(x) < 1 + (x in special_gear_numbers):
            set_of_used_ratios_this_line.append(x)
    
    # represents the numbers in the row of symbols - there should be the same number of these as gear ratios
    part_numbers_in_this_row = [int(i) for i in "".join(row).split(".") if i]
    assert len(part_numbers_in_this_row) == len(set_of_used_ratios_this_line)

    # add each part number to the correct bucket
    for gear_ratio, part_number in zip(set_of_used_ratios_this_line, part_numbers_in_this_row):
        ratios_to_numbers[gear_ratio].append(part_number)


# for each gear, assuming it has two corresponding numbers, compute the product and add it to the answer to pt. 2
for gear_ratio in ratios_to_numbers:
    if len(ratios_to_numbers[gear_ratio]) == 2:
        answer_part_2 += ratios_to_numbers[gear_ratio][0] * ratios_to_numbers[gear_ratio][1]

# output the answers
output(answer_part_1)
output(answer_part_2)
