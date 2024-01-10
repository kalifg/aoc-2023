import sys
from range import Range
from shared import input
from transformer import Transformer


def generate_seeds(seed_params):
    seed_groups = [(seed_params[i], seed_params[i + 1]) for i in range(0, len(seed_params), 2)]
    # print(seed_groups)

    # seeds = [list(range(group[0], group[0] + group[1])) for group in seed_groups]
    # seeds = [seed for seed_list in seeds for seed in seed_list]
    seeds = [Range(sg[0], sg[1]) for sg in seed_groups]
    # print(seeds)

    return seeds

def parse_lines(lines):
    seeds = []
    sections = {}
    source = None
    idx = 0

    for line in lines:
        line = line.strip()

        if line.startswith('seeds:'):
            seeds = generate_seeds([int(seed) for seed in line.split(': ')[1].split(' ')])
        elif line.endswith(':'):
            section_name = line[:-5]
            source, _, destination = section_name.split('-')

            if section_name not in sections:
                sections[source] = {
                    'idx': idx,
                    'source': source,
                    'destination': destination,
                    'transformer': Transformer(source, destination),
                }

                idx += 1
        elif not line:
            continue
        else:
            sections[source]['transformer'].add_mapping(*[int(num) for num in line.split(' ')])

    # print(seeds)
    # print(sections)

    transformers = []
    source = 'seed'

    while source in sections:
        transformers.append(sections[source]['transformer'])
        source = sections[source]['destination']

    # for transformer in transformers:
    #     print(transformer)

    # print(seeds)
    destinations = seeds

    for transformer in transformers:
        # print(f'Applying {transformer} to {destination}', end='')
        destinations = transformer.transform(destinations)
        # print(f'->{destination}')

    print(seeds)
    print(len(seeds))
    print(destinations)
    print(len(destinations))
    print(destinations[0].source)
    # print(min(destinations))

# 861012996 is too high (was accidentally only looking at 2 sets of seeds)
# 136096660 is right!
def main(filename):
    lines = input.readfile(filename)
    parse_lines(lines)


if __name__ == '__main__':
    main(sys.argv[1])