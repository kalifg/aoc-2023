import collections
import sys
sys.path.append('../shared')

from shared import input

Turn = collections.namedtuple('Turn', 'red green blue')
Game = collections.namedtuple('Game', 'id turns')
Bag = collections.namedtuple('Bag', 'red green blue')


def process_turn(turn):
    counts = turn.split(', ')
    args = {
        'red': 0,
        'green': 0,
        'blue': 0,
    }

    for count in counts:
        number, color = count.split(' ')
        args[color] = int(number)

    return Turn(**args)


def process_line(line):
    game_id, turns = line.split(': ')
    game_id = int(game_id.split(' ')[1])

    turns = [process_turn(turn) for turn in turns.split('; ')]

    return Game(id=game_id, turns = turns)


def load_games(filename):
    lines = input.readfile(filename)
    games = [process_line(line) for line in lines]

    return games


def is_valid_turn(bag, turn):
    return bag.red >= turn.red and bag.green >= turn.green and bag.blue >= turn.blue


def is_valid_game(bag, game: Game):
    for turn in game.turns:
        if not is_valid_turn(bag, turn):
            return False

    return True


def compute_minimum_bag(game):
    counts = {
        'red': 0,
        'green': 0,
        'blue': 0,
    }
    
    for turn in game.turns:
        counts['red'] = max(counts['red'], turn.red)
        counts['green'] = max(counts['green'], turn.green)
        counts['blue'] = max(counts['blue'], turn.blue)

    return Bag(**counts)


def compute_bag_power(bag):
    return bag.red * bag.green * bag.blue


def main():
    # bag = Bag(red=12, green=13, blue=14)
    games_to_check = load_games(sys.argv[1])
    # valid_games = filter(lambda game: is_valid_game(bag, game), games_to_check)
    minimum_bags = [compute_minimum_bag(game) for game in games_to_check]
    powers = [compute_bag_power(bag) for bag in minimum_bags]

    print(sum(powers))
    # print(sum([game.id for game in valid_games]))


if __name__ == '__main__':
    main()