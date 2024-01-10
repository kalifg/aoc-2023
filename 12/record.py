def get_runs(springs, chars):
    runs = []
    current_run = []
    current_run_start = None

    for i, c in enumerate(springs):
        if c in chars:
            if current_run_start is None:
                current_run_start = i

            current_run.append(c)
        else:
            if current_run_start is not None:
                runs.append((current_run_start, current_run))
                current_run_start = None
                current_run = []

    if current_run_start is not None:
        runs.append((current_run_start, current_run))

    return runs


class Record:
    def __init__(self, springs, damage_runs):
        self.springs = springs
        self.damage_runs = damage_runs

    def __repr__(self):
        return f'<{"".join(self.springs)} {self.damage_runs}>'

    def get_possible_run_locations(self):
        return [(run, self.get_possible_locations(idx)) for idx, run in enumerate(self.damage_runs)]

    def get_possible_locations(self, idx):
        starts = get_run_starts(self.damage_runs, idx, self.springs)
        # print(starts)

        possible_locations = [location for location in starts
                              if self.is_valid_run_location(idx, location)]
        # print(possible_locations)

        return possible_locations

    def is_certain_run_location(self, run, start):
        return '#' in self.springs[start:start + run]

    def is_valid_run_location(self, run_index, start):
        run = self.damage_runs[run_index]

        if '.' in self.springs[start:start + run]:
            return False

        if start + run < len(self.springs) and self.springs[start + run] == '#':
            return False

        if start > 0 and self.springs[start - 1] == '#':
            return False

        damage_runs = self.damage_runs[:run_index]
        visible_runs = [len(r) for _, r in get_runs(self.springs[:start], '#')]

        if has_invalid_runs(visible_runs, damage_runs):
            # print('before:', run_index, run, damage_runs, start, visible_runs)
            return False

        damage_runs = self.damage_runs[run_index + 1:]
        visible_runs = [len(r) for _, r in get_runs(self.springs[start + run:], '#')]

        if has_invalid_runs(visible_runs, damage_runs):
            # print('after:', run_index, run, damage_runs, start, visible_runs)
            return False

        return True


def get_run_starts(runs, idx, springs):
    before_runs = runs[:idx]
    run = runs[idx]
    after_runs = runs[idx + 1:]

    smallest_possible_before = get_smallest_chunk(springs, before_runs)
    lowest_possible = len(smallest_possible_before)

    highest_possible_after = list(reversed(get_smallest_chunk(list(reversed(springs)), list(reversed(after_runs)))))
    highest_possible = len(springs) - len(highest_possible_after) - run

    # print([before_runs, run, after_runs])
    # print(smallest_possible_before, lowest_possible)
    # print(highest_possible_after, highest_possible)

    return list(range(lowest_possible, highest_possible + 1))


def get_smallest_chunk(springs, before_runs):
    chunk = []

    operational = len(before_runs)
    possibly_damaged = sum(before_runs)

    if operational == possibly_damaged == 0:
        return chunk

    if len(before_runs) > 1:
        first_smallest = get_smallest_chunk(springs, [before_runs[0]])
        remaining = get_smallest_chunk(springs[len(first_smallest):], before_runs[1:])

        return first_smallest + remaining

    operational_count = 0
    possibly_damaged_count = 0
    last_run = 0
    current_run = 0

    for spring in springs:
        chunk.append(spring)
        if spring == '.':
            operational_count += 1 if possibly_damaged_count > 0 else 0
            last_run = current_run
            current_run = 0
        else:
            possibly_damaged_count += 1
            current_run += 1

        if spring == '#':
            continue

        if (possibly_damaged_count >= possibly_damaged and
                (operational_count + possibly_damaged_count - possibly_damaged) >= operational):
            if current_run:
                if current_run > before_runs[-1]:
                    return chunk
            elif last_run >= before_runs[-1]:
                return chunk

    return chunk


def has_invalid_runs(visible_runs, damage_runs):
    if not damage_runs and visible_runs:
        return True

    for d in sorted(set(visible_runs)):
        if max(damage_runs) < d:
            return True

        if max(damage_runs) == d and visible_runs.count(d) > damage_runs.count(d):
            return True

    return False
