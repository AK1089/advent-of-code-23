from aocutil import read, output, submit
data = read(__file__).splitlines()

# number of points you get by the part 1 scoring rule, and the number of each scratchcard you have for part 2
total_scratchcard_points = 0
quantities = {i: 1 for i in range(1, len(data) + 1)}

# for each scratchcard, split it down the bar into the winners and what you have
for cardnum, line in enumerate(data, 1):
    winners, ticket = line.split(":")[1].split("|")

    # turn these into sets of numbers
    winners = set(winners.split())
    ticket = set(ticket.split())

    # matches are the overlap between winners and haves, and the scoring rule is as follows
    matches = len(winners.intersection(ticket))
    total_scratchcard_points += int(2 ** (matches - 1))

    # for each match, add to the following card, once for each one of *this* card you have
    for i in range(cardnum + 1, cardnum + matches + 1):
        quantities[i] += quantities[cardnum]

# outputs the answers
output(total_scratchcard_points)
output(sum(quantities.values()))
