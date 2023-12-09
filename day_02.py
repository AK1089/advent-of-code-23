from aocutil import read, output, submit
data = read(__file__).splitlines()

# the answers to parts 1 and 2 (possible games). possible_games are the ids 1-100, and the total power is as-yet 0.
possible_games = [i for i in range(1, 101)]
total_power = 0

# for each game, get the game ID ("Game #") and the setup (rest of line after ": ") and initialise min required cubes to (0, 0, 0)
for line in data:
    game_id, setup = line.split(": ")
    min_b = min_g = min_r = 0

    # in each round of displaying cubes, look at each type (eg. "3 blue") individually
    for displayed_cubes in setup.split("; "):
        for subset in displayed_cubes.split(", "):

            # get the number and colour we're being shown
            number, colour = subset.split()
            number = int(number)

            # pt. 1: 12 red / 13 green / 14 blue cubes - if we break any of these limits then remove this game from the possible games
            if (number > 12 and colour == "red") or (number > 13 and colour == "green") or (number > 14 and colour == "blue"):

                # take the game ID ("Game 12"), extract the number, and set that index to 0 (to denote not possible)
                possible_games[int(game_id.split()[1]) - 1] = 0

            # update the minimum required number of red / blue / green cubes as needed
            if colour == "red":
                min_r = max(min_r, number)
            elif colour == "blue":
                min_b = max(min_b, number)
            elif colour == "green":
                min_g = max(min_g, number)

    # add the power of this game to the total power    
    total_power += min_g * min_b * min_r


# answers to parts 1 & 2 - possible_games only has the IDs of the not-flagged-as-impossible games, and total_power is just the answer
output(sum(possible_games))
output(total_power)
