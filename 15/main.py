import sys

from shared import input


class Instruction:
    def __init__(self, instruction):
        if '=' in instruction:
            self.label, focal_length = instruction.split('=')
            self.focal_length = int(focal_length)
        elif '-' in instruction:
            self.focal_length = None
            self.label = instruction[:-1]

        self.box = hash_step(self.label)

    def __repr__(self):
        return f'{self.label}{"=" if self.focal_length else "-"}{self.focal_length if self.focal_length else ""} {self.box}'


class Lens:
    def __init__(self, label, focal_length):
        self.label = label
        self.focal_length = focal_length

    def __repr__(self):
        return f'[{self.label} {self.focal_length}]'

    def __eq__(self, other):
        return other.label == self.label


class Box:
    def __init__(self, number):
        self.number = number
        self.slots = []

    def __repr__(self):
        return f'{self.slots}'

    def __contains__(self, lens):
        return lens in self.slots

    def __len__(self):
        return len(self.slots)

    def remove(self, lens):
        self.slots.remove(lens)

    def append(self, lens):
        self.slots.append(lens)

    def replace(self, lens):
        self.slots[self.slots.index(lens)] = lens

    def powers(self):
        return [(self.number + 1) * (i + 1) * lens.focal_length for i, lens in enumerate(self.slots)]


def print_boxes(boxes):
    print([f'{i}: {box}' for i, box in enumerate(boxes) if box])


# 519603 is right
#
# 244342 is right
def main(filename):
    line = ''.join(input.readfile(filename))
    steps = line.split(',')
    print(steps)

    boxes = []

    for i in range(256):
        boxes.append(Box(i))

    instructions = [Instruction(step) for step in steps]
    print(instructions)

    for instruction in instructions:
        box = boxes[instruction.box]
        lens = Lens(instruction.label, None)

        if instruction.focal_length:
            lens = Lens(instruction.label, instruction.focal_length)

            if lens in box:
                box.replace(lens)
            else:
                box.append(lens)
        else:
            if lens in box:
                box.remove(lens)

    print_boxes(boxes)

    powers = [box.powers() for box in boxes if box]
    print(powers)

    print(f'Total: {sum([sum(box) for box in powers])}')


def hash_step(step):
    value = 0

    for c in step:
        value += ord(c)
        value *= 17
        value %= 256

    return value


if __name__ == '__main__':
    main(sys.argv[1])
