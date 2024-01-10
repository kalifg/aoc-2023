from shared import input

lines = input.readfile('sprites.txt')
sprites = {}

for i in range(0, len(lines), 9):
    if len(lines[i]) < 1:
        break

    sprites[lines[i][0]] = lines[i + 1:i + 9]

print(sprites)
sprite_res = len(sprites['.'][0])

class Node:
    def __init__(self, type, location):
        self.type = type
        self.is_start = type == 'S'
        self.location = location
        self.distance = -1
        self.paths = {}
        self.inside = [None, None, None, None]

    def __repr__(self):
        # return f'<"{self.type}"@{self.location}∂{self.distance}, {self.paths}>'
        return f'<"{self.type}"@{self.location}∂{self.distance}>'

    def __eq__(self, other):
        return other.location == self.location

    def add_paths(self, adjacent_nodes):
        self.paths = adjacent_nodes

        for direction, node in self.paths.items():
            if node and node.distance < 0:
                node.distance = self.distance + 1
                
        if self.is_start:
            if adjacent_nodes['left'] and adjacent_nodes['right']:
                self.type = '-'
            elif adjacent_nodes['left'] and adjacent_nodes['up']:
                self.type = 'J'
            elif adjacent_nodes['left'] and adjacent_nodes['down']:
                self.type = '7'
            elif adjacent_nodes['right'] and adjacent_nodes['up']:
                self.type = 'L'
            elif adjacent_nodes['right'] and adjacent_nodes['down']:
                self.type = 'F'
            elif adjacent_nodes['up'] and adjacent_nodes['down']:
                self.type = '|'

    def get_path(self, came_from):
        valid_paths = [node for direction, node in self.paths.items() if node and node != came_from]

        if len(valid_paths) > 1:
            raise RuntimeError(f'Multiple valid paths found for {self} coming from {came_from}')

        return valid_paths[0]

    def on_path(self):
        return self.distance > -1

    def paint(self, upper, lower):
        if not self.on_path() or self.type == '-':
            self.inside = [upper, upper, lower, lower]
        elif self.type in ['F', '7']:
            self.inside = [upper, upper, lower, not lower]
        elif self.type in ['J', 'L']:
            self.inside = [upper, not upper, lower, lower]
        elif self.type == '|':
            self.inside = [upper, not upper, lower, not lower]

    def is_inside(self):
        return not self.on_path() and all(self.inside)

    def paint_image(self, img, start):
        grey = (255, 255, 255) if self.is_start else (128, 128, 128)
        green = (0, 128, 0) if self.on_path() else (0, 255, 0)
        black = (0, 0, 0)
        a, b = start

        type = self.type if self.type in sprites else '.'

        for y, row in enumerate(sprites[type]):
            for x, pixel in enumerate(row):
                quadrant = int(x // (sprite_res / 2)) + int(y // (sprite_res / 2)) * 2
                inside = self.inside[quadrant]
                color = grey if pixel == '*' else (green if inside else black)
                img.putpixel((a + x, b + y), color)

