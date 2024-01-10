def join_tiles(tiles):
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            tile.x = x
            tile.y = y

            if x < len(row) - 1:
                tile.right = tiles[y][x + 1]

            if x > 0:
                tile.left = tiles[y][x - 1]

            if y < len(tiles) - 1:
                tile.below = tiles[y + 1][x]

            if y > 0:
                tile.above = tiles[y - 1][x]

class Tile:
    opposites = {
        'left': 'right',
        'right': 'left',
        'above': 'below',
        'below': 'above',
    }

    exits = {
        '.': {
            'left': ['right'],
            'right': ['left'],
            'above': ['below'],
            'below': ['above'],
        },
        '/': {
            'left': ['above'],
            'right': ['below'],
            'above': ['left'],
            'below': ['right'],
        },
        '\\': {
            'left': ['below'],
            'right': ['above'],
            'above': ['right'],
            'below': ['left'],
        },
        '-': {
            'left': ['right'],
            'right': ['left'],
            'above': ['left', 'right'],
            'below': ['left', 'right'],
        },
        '|': {
            'left': ['above', 'below'],
            'right': ['above', 'below'],
            'above': ['below'],
            'below': ['above'],
        },
    }

    def __init__(self, device):
        self.device = device

        self.entered_from = {
            'left': 0,
            'right': 0,
            'above': 0,
            'below': 0,
        }

        self.left = None
        self.right = None
        self.above = None
        self.below = None

        self.x = None
        self.y = None

    def __repr__(self):
        return f'{self.device} {(self.x, self.y)}'

    def reset(self):
        for direction in self.entered_from.keys():
            self.entered_from[direction] = 0

    def enter_from(self, direction):
        if self.entered_from[direction] > 0:
            return []

        self.entered_from[direction] += 1
        exits = self.exits[self.device][direction]

        return [(self.opposites[exit], getattr(self, exit)) for exit in exits]

    def is_energized(self):
        return bool(sum([times for direction, times in self.entered_from.items()]))
