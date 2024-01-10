import math
from typing import List, Optional


class Block:
    opposites = {
        'left': 'right',
        'up': 'down',
        'down': 'up',
        'right': 'left',
    }

    def __init__(self, heat_loss, location):
        self.tentative_distance = math.inf
        self.heat_loss = int(heat_loss)
        self.last_turned = 1

        self.direction = None
        self.previous_block: Optional[Block] = None

        self.left = None
        self.right = None
        self.up = None
        self.down = None

        self.x, self.y = location

    def __repr__(self):
        return f'{self.tentative_distance} {self.heat_loss} {self.direction} {self.last_turned} {(self.x, self.y)}'

    def __lt__(self, other):
        return self.tentative_distance < other.tentative_distance

    @property
    def neighbors(self):
        return {
            'left': self.left,
            'right': self.right,
            'up': self.up,
            'down': self.down,
        }

    def reset(self):
        self.tentative_distance = math.inf
        self.last_turned = 1
        self.direction = None

    def get_direction(self, path):
        if len(path) < 2:
            return 'left'
        else:
            block = path[-2]
    
        if self.y == block.y:
            if self.x == block.x + 1:
                return 'left'
            elif self.x == block.x - 1:
                return 'right'
        elif self.x == block.x:
            if self.y == block.y + 1:
                return 'up'
            elif self.y == block.y - 1:
                return 'down'

        return None


def reset_blocks(blocks):
    for row in blocks:
        for block in row:
            block.reset()


def print_block_show_direction(block):
    if block.direction:
        if block.direction == 'left':
            print('>', end='')
        elif block.direction == 'right':
            print('<', end='')
        elif block.direction == 'up':
            print('v', end='')
        elif block.direction == 'down':
            print('^', end='')
    else:
        print(block.heat_loss, end='')


def print_blocks(blocks):
    for row in blocks:
        for block in row:
            print_block_show_direction(block)
        print()
    print()


class Path:
    def __init__(self, blocks=None):
        if blocks is None:
            blocks = []

        self.heat_loss = sum([block.heat_loss for block in blocks[1:]])
        self.blocks = blocks

    def __repr__(self):
        return f'<Path heat_loss: {self.heat_loss}, start: {self.blocks[0]}, end: {self.blocks[-1]}, length: {len(self.blocks)}>'

    def __add__(self, block_list_of_blocks_or_path):
        if isinstance(block_list_of_blocks_or_path, Block):
            return Path(self.blocks + [block_list_of_blocks_or_path])
        elif isinstance(block_list_of_blocks_or_path, List):
            return Path(self.blocks + block_list_of_blocks_or_path)
        elif isinstance(block_list_of_blocks_or_path, Path):
            return Path(self.blocks + block_list_of_blocks_or_path.blocks)
        else:
            raise TypeError

    def __len__(self):
        return len(self.blocks)

    def __getitem__(self, item):
        return self.blocks[item]

    def __contains__(self, block):
        return block in self.blocks

    def __bool__(self):
        return bool(self.blocks) and bool(self.blocks[-1])

    def __eq__(self, other):
        return self.blocks == other.blocks

    @property
    def ends_in_three_straight(self):
        if len(self.blocks) > 3:
            return (self.blocks[-1].x == self.blocks[-2].x == self.blocks[-3].x == self.blocks[-4].x or
                    self.blocks[-1].y == self.blocks[-2].y == self.blocks[-3].y == self.blocks[-4].y)

        return False
