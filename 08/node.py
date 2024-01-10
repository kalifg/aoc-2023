class Node:
    def __init__(self, name:str, destinations):
        self.name = name
        self.start_node = name.endswith('A')
        self.end_node = name.endswith('Z')
        self.left, self.right = destinations

    def __repr__(self):
        return f'{self.name} -> ({self.left.name}, {self.right.name})'

    def take(self, direction):
        if direction == 'L':
            return self.left
        elif direction == 'R':
            return self.right

    def take_str(self, direction):
        if direction == 'L':
            return f'([{self.left.name}],  {self.right.name} )'
        elif direction == 'R':
            return f'( {self.left.name} , [{self.right.name}])'
