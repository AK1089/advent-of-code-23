from aocutil import read, output, submit
data = read(__file__).splitlines()

# cards sorted from best to worst using the old and new rules
CARD_ORDERING_OLD_RULES = "AKQJT98765432"
CARD_ORDERING_NEW_RULES = "AKQT98765432J"

# this is a function to get a (sparse) rank-order of the hands (lower is a better hand)
# ties broken by best-to-worst special hand, then cards in order of how good they are / their position
# original_hand is optional, for part 2 hands (it's the hand without the Jokers being replaced)
def get_ordering(hand: str, original_hand: str = None):

    # if we've provided an original (ie. using new rules) and there's a Joker, try replacing it with everything else and see what
    # gets the best score. (this is, of course, recursed upon, with the same original hand, if necessary)
    if original_hand and "J" in hand:
        return min((get_ordering(hand.replace("J", x, 1), original_hand) for x in CARD_ORDERING_OLD_RULES.replace("J", "")))

    # the rest of the procedure is the same regardless. this first bit is the overarching thing: the type of hand

    if len(set(hand)) == 1:                                                       # five of a kind [5]
        order = 0
    elif len(set(hand)) == 2 and hand.count(hand[0]) in (1, 4):                   # four of a kind [4-1]
        order = 1000000
    elif len(set(hand)) == 2 and hand.count(hand[0]) in (2, 3):                   # full house [3-2]
        order = 2000000
    elif len(set(hand)) == 3 and all((hand.count(x) in (1, 3) for x in hand)):    # three of a kind [3-1-1]
        order = 3000000
    elif len(set(hand)) == 3:                                                     # pair [2-2-1]
        order = 4000000
    elif len(set(hand)) == 4:                                                     # pair [2-1-1-1]
        order = 5000000
    elif len(set(hand)) == 5:                                                     # pair [2-1-1-1]
        order = 6000000

    # if we've provided an "original" hand, then we're using the new (part 2) rules
    card_sorting_order = CARD_ORDERING_NEW_RULES if original_hand else CARD_ORDERING_OLD_RULES
    hand_to_sort = original_hand or hand

    # basically converting into tridecimal and adding a five tridigit number on (doesn't mess with the hand orderings, as 13^5 < 10^6)
    order += (13 ** 4) * card_sorting_order.index(hand_to_sort[0])
    order += (13 ** 3) * card_sorting_order.index(hand_to_sort[1])
    order += (13 ** 2) * card_sorting_order.index(hand_to_sort[2])
    order += (13     ) * card_sorting_order.index(hand_to_sort[3])
    order +=             card_sorting_order.index(hand_to_sort[4])

    # this is how good this hand is! higher numbers will definitely be worse, lower numbers will definitely be better
    return order


# let's store the orderings by each ranking system in these (as well as the hands and the bids)
orderings_part_1, orderings_part_2 = [], []
bids = []

# for each hand, let's log its corresponding bid and how well it fares by each scoring system
for line in data:
    hand, bid = line.split()
    bids.append(int(bid))

    # each scoring system's evaluation of the hands
    orderings_part_1.append(get_ordering(hand))
    orderings_part_2.append(get_ordering(hand, hand))

# the final answers to each part
part_1_answer = part_2_answer = 0

# let's go by each sorting system. the score that each hand gets is the total minus the (0-indexed) position it sits in
# within the ordered list, which is hand_ordering here. we then have to find the bid that's in that position and multiply
for hand_ordering, hand_score in enumerate(sorted(orderings_part_1)):
    part_1_answer += (len(data) - hand_ordering) * bids[orderings_part_1.index(hand_score)]
for hand_ordering, hand_score in enumerate(sorted(orderings_part_2)):
    part_2_answer += (len(data) - hand_ordering) * bids[orderings_part_2.index(hand_score)]

# outputs our answers!
output(part_1_answer)
output(part_2_answer)
