class Cover:
    def __init__(self, left, intersect):
        self.left = left
        self.intersect = intersect

    def __eq__(self, other) -> bool:
        return self.left == other.left and self.intersect == other.intersect

    def __repr__(self):
        return f'<{self.left}, {self.intersect}>'


