from cover import Cover


class Range:
    @classmethod
    @property
    def empty_set(cls):
        return Range(0, 0)

    def __init__(self, source, length):
        self.source = source
        self.length = length

    def __repr__(self):
        if self == self.empty_set:
            return '<Empty>'
        else:
            return f'<{self.source}, {self.source + self.length - 1}>'

    def __bool__(self):
        return self != self.empty_set

    def __eq__(self, other):
        return (self.source == other.source and self.length == other.length) or (self.length == 0 and other.length == 0)

    def cover(self, other) -> Cover:
        other_idx = 0 if other.source <= self.source else 1
        ranges = sorted([self, other], key=lambda r: r.source)

        if ranges[0].max < ranges[1].source:
            return Cover(ranges[other_idx], Range.empty_set)
        elif ranges[0].max >= ranges[1].max:
            return Cover(Range.empty_set, other)
        else:
            left = Range(ranges[0].source, ranges[1].source - ranges[0].source) if other_idx == 0 else Range(ranges[0].max + 1, ranges[1].max - ranges[0].max)
            return Cover(left, Range(ranges[1].source, ranges[0].max - ranges[1].source + 1))

    @property
    def max(self):
        return self.source + self.length - 1

