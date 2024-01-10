import sys

sys.path.append('../shared')

from card import Card
from shared import input


# 5329815 is right
def main(filename):
    lines = input.readfile(filename)
    cards = [process_line(line) for line in lines]
    # print(sum([card.score() for card in cards]))

    card_stack = []
    cards_in_play = cards

    while True:
        # for card in cards_in_play:
        new_cards = [card for pulled_cards in [pull_cards(cards, card) for card in cards_in_play] for card in pulled_cards]
        card_stack += cards_in_play
        # print(new_cards)
        if len(new_cards) > 0:
            cards_in_play = new_cards
        else:
            break

    # for card in card_stack:
    #     print(card)

    print(len(card_stack))


def pull_cards(cards, card):
    return cards[card.id:card.id + card.count_wins()]


def process_line(line):
    part = line.split(':')
    card_id = int(list(filter(None, part[0].split(' ')))[1])
    numbers = part[1].split(' | ')
    winning_numbers = [int(num) for num in numbers[0].split(' ') if num.isnumeric()]
    card_numbers = [int(num) for num in numbers[1].split(' ') if num.isnumeric()]

    return Card(card_id, winning_numbers, card_numbers)


if __name__ == '__main__':
    main(sys.argv[1])