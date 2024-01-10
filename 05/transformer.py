from range import Range
from typing import List


class MappingRange(Range):
    def __init__(self, destination, source, length):
        super().__init__(source, length)
        self.destination = destination

    @property
    def offset(self):
        return self.destination - self.source

    def map(self, source_range):
        cover = self.cover(source_range)
        unmapped = [cover.left]
        mapped = None

        if (cover.intersect):
            mapped = Range(cover.intersect.source + self.offset, cover.intersect.length)

        return mapped, unmapped

    def __repr__(self):
        return f'<{self.source}, {self.max}> -> <{self.destination}, {self.destination + self.length - 1}> (offset {self.offset})'


class Transformer:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        self.mappings:List[MappingRange] = []

    def add_mapping(self, destination, source, length):
        self.mappings.append(MappingRange(destination, source, length))
        self.mappings = sorted(self.mappings, key=lambda mapping: mapping.source)

    def transform(self, sources):
        mapped = []
        unmapped = list(sources)

        for mapping in self.mappings:
            for leftover_source in list(unmapped):
                done, not_done = mapping.map(leftover_source)

                if done:
                    unmapped.remove(leftover_source)
                    unmapped += not_done
                    mapped.append(done)

        return sorted(filter(None, mapped + unmapped), key=lambda r: r.source)

    def __repr__(self):
        return repr(f'{self.source}->{self.destination}: {self.mappings}')
