import math


class Race:
    def __init__(self, time, record_distance):
        self.time = time
        self.record_distance = record_distance

    def __repr__(self):
        return f'<Time: {self.time}ms, Record Distance: {self.record_distance}mm>'

    def ways_to_win(self):
        # distance = b * (t - b) = bt - b^2
        # bt - b^2 >= r + 1
        # bt - b^2 - r - 1 > 0
        # b^2 - bt + r + 1 < 0
        # b₁ = (t + √(t^2 - 4(r + 1))) / 2
        # b₂ = (t - √(t^2 - 4(r + 1))) / 2
        d = math.sqrt(self.time**2 - 4*(self.record_distance + 1))
        b1 = (self.time + d) / 2
        b2 = (self.time - d) / 2

        return math.floor(b1) - math.ceil(b2) + 1
    