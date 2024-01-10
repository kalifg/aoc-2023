import sys
from shared import input
from cards import Card, Hand


def process_line(line):
    hand_string, bid_string = line.split(' ')
    cards = [Card(label) for label in hand_string]

    return Hand(cards, int(bid_string))


def main(filename):
    lines = input.readfile(filename)
    hands = sorted([process_line(line) for line in lines])

    # for hand in hands:
    #     print(hand)

    winnings = [(idx + 1) * hand.bid for idx, hand in enumerate(hands)]

    # print(winnings)
    print(sum(winnings))


# 249390788 is
# 249087516 is too low
# 248974049
# 248672737
# 248440116 is too low

# 249733832 is too high
# 248750248 is right!
# 248621432 is too low
if __name__ == '__main__':
    main(sys.argv[1])