import math
import re
import sys

from enum import Enum
from shared import input
from typing import Union, Dict, Optional, List


class Comparison(Enum):
    LT = 0
    GT = 2

    def __repr__(self):
        match self.name:
            case 'GT':
                return '>'
            case 'LT':
                return '<'

    def __call__(self, *args, **kwargs):
        if self == Comparison.LT:
            return args[0] < args[1]

        if self == Comparison.GT:
            return args[0] > args[1]

    def __neg__(self):
        match self:
            case Comparison.LT:
                return Comparison.GT

            case Comparison.GT:
                return Comparison.LT


class Action(Enum):
    NONE = 0
    R = 1
    A = 2

    def __repr__(self):
        return self.name


class Part:
    def __init__(self, x: int, m: int, a: int, s: int):
        self.x = int(x)
        self.m = int(m)
        self.a = int(a)
        self.s = int(s)

    def rating(self) -> int:
        return self.x + self.m + self.a + self.s

    def __repr__(self):
        return f'<Part: {{x={self.x},m={self.m},a={self.a},s={self.s}}}>'


class Workflow:
    def __init__(self, name: str):
        self.name = name
        self.default = None
        self.rules = []

    def __repr__(self):
        return f'<Workflow: {self.name}, Default: {repr(self.default)}, Rules: {self.rules}>'

    def __call__(self, part: Part) -> Union['Action', 'Workflow']:
        for rule in self.rules:
            if rule.comparison(getattr(part, rule.attribute), rule.value):
                return rule.action

        return self.default


class Range:
    MIN = 1
    MAX = 4000

    def __init__(self, min_value: Optional[int] = None, max_value: Optional[int] = None):
        min_value = Range.MIN if not min_value else min_value
        max_value = Range.MAX if not max_value else max_value

        if min_value > max_value:
            raise ValueError('Min value greater than max value')

        if min_value < Range.MIN:
            raise ValueError('Invalid min value, out of range')

        if max_value > Range.MAX:
            raise ValueError('Invalid max value, out of range')

        self._min = min_value
        self._max = max_value

    def __repr__(self):
        return repr((self._min, self._max))

    def __int__(self):
        return self._max - self._min + 1

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, value):
        if value < Range.MIN:
            raise ValueError('Invalid min value, out of range')

        if value > self._max:
            raise ValueError('Min value greater than max value')

        self._min = value

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, value):
        if value > Range.MAX:
            raise ValueError('Invalid max value, out of range')

        if value < self._min:
            raise ValueError('Max value less than min value')

        self._max = value


class Ranges:
    def __init__(self):
        self.ranges = {
            'x': Range(),
            'm': Range(),
            'a': Range(),
            's': Range(),
        }

    def __repr__(self):
        return repr(self.ranges)

    def __call__(self, rule: 'Rule'):
        current_range = self.ranges[rule.attribute]

        match rule.comparison:
            case Comparison.LT:
                current_range.max = min(current_range.max, rule.value) - 1
            case Comparison.GT:
                current_range.min = max(current_range.min, rule.value) + 1

        return self

    def __int__(self):
        return math.prod([int(r) for r in self.ranges.values()])


class Rule:
    def __init__(self, attribute: str, comparison: Comparison, value: int, action: Action | Workflow):
        self.attribute = attribute
        self.comparison = comparison
        self.value = value
        self.action = action

    def __repr__(self):
        return f'{self.attribute}{repr(self.comparison)}{self.value}:{self.action.name}'

    def __neg__(self):
        return Rule(self.attribute, -self.comparison, self.value - 1 if self.comparison == Comparison.LT else self.value + 1, Action.NONE)


# 401674 is correct
#
# 134906204068564 is correct
def main(filename):
    lines = input.readfile(filename)
    parts, workflows = process_lines(lines)

    # print(parts)
    # print()

    for workflow in workflows.values():
        print(workflow)

    print()

    # accepted = []
    #
    # for part in parts:
    #     print(f'{part}: ', end='')
    #     workflow = workflows['in']
    #     print(workflow.name, end='')
    #
    #     while True:
    #         workflow = workflow(part)
    #         print(f' -> {workflow.name}', end='')
    #
    #         if isinstance(workflow, Action):
    #             if workflow == Action.A:
    #                 accepted.append(part)
    #
    #             break
    #
    #     print()
    #
    # print()
    # print(accepted)
    # print(f'Total: {sum([part.rating() for part in accepted])}')

    accepted_tails = []
    accepted_heads = []
    workflow = workflows['in']
    graph = graph_workflow(workflow, accepted_paths=accepted_tails)

    # print(graph)
    # print()

    for accepted_tail in accepted_tails:
        # print(accepted_tail)
        head = accepted_tail
        path = [(head['parent']['name'] if head['parent'] else None, head['rule'], head['previous_rules'], head['action'])]

        while head['parent']:
            path.insert(0, (head['parent']['parent']['name'] if head['parent']['parent'] else None, head['parent']['rule'], head['parent']['previous_rules'], head['parent']['name']))
            head = head['parent']

        # print(head)
        accepted_heads.append(path)

        print()

    print()

    total_combinations = 0
    paths = []

    for accepted_head in accepted_heads:
        current_ranges = Ranges()
        path = []

        for parent, rule, previous_rules, target in accepted_head[1:]:
            path.append((parent, f'default({target})' if rule == 'default' else rule))

            for pr in previous_rules:
                current_ranges = current_ranges(-pr)

            current_ranges = current_ranges if rule == 'default' else current_ranges(rule)

            print(parent, rule, target, current_ranges, f'{int(current_ranges):,}')

        paths.append((path, current_ranges, int(current_ranges)))
        total_combinations += int(current_ranges)

        print()

    for path in paths:
        print(path)

    print()
    # print(f'Total combinations: {167409079868000}')
    print(f'Total combinations: {total_combinations}')
    print(f'Total combinations: {total_combinations:,}')


def graph_workflow(workflow: Union[Action, Workflow], rule: Optional[Rule] = None, previous_rules: Optional[List[Rule]] = None, parent_graph: Optional[Dict] = None, accepted_paths: List[Dict] = None) -> Dict | Action:
    previous_rules = previous_rules[:] if previous_rules else []

    if isinstance(workflow, Action):
        d = {
            'action': workflow,
            'parent': parent_graph,
            'rule': rule,
            'previous_rules': previous_rules,
        }

        if workflow == Action.A:
            accepted_paths.append(d)

        return d

    graph = {
        'name': workflow.name,
        'parent': parent_graph,
        'rule': rule,
        'previous_rules': previous_rules,
    }

    previous_rules = []

    for rule in workflow.rules:
        graph[rule] = graph_workflow(rule.action, rule, previous_rules, graph, accepted_paths)
        previous_rules.append(rule)

    graph['default'] = graph_workflow(workflow.default, 'default', previous_rules, graph, accepted_paths)

    return graph


def process_lines(lines):
    workflows = {}
    parts = []

    for line in lines:
        matches = re.finditer(
            r'(?P<name>\w+)\{|(?P<attribute>[xmas])(?P<comparison>[<>])(?P<value>\d+):(?P<action>\w+)|,(?P<default>\w+)\}',
            line)
        name = default = None
        rules = []

        for match in matches:
            if match.group('name'):
                name = match.group('name')
            elif match.group('attribute'):
                rules.append({
                    'attribute': match.group('attribute'),
                    'comparison': Comparison.LT if match.group('comparison') == '<' else Comparison.GT,
                    'value': int(match.group('value')),
                    'action': getattr(Action, match.group('action')) if match.group('action') in ['A',
                                                                                                  'R'] else match.group(
                        'action'),
                })
            elif match.group('default'):
                match match.group('default'):
                    case 'A' | 'R':
                        default = getattr(Action, match.group('default'))
                    case _:
                        default = match.group('default')

        if name:
            workflow = Workflow(name)
            workflow.default = default

            for rule in rules:
                workflow.rules.append(Rule(rule['attribute'], rule['comparison'], rule['value'], rule['action']))

            workflows[name] = workflow

        match = re.match(r'\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}', line)

        if match:
            parts.append(Part(*match.groups()))

    for workflow in workflows.values():
        if not isinstance(workflow.default, Action):
            workflow.default = workflows[workflow.default]

        for rule in workflow.rules:
            if isinstance(rule.action, Action):
                continue

            rule.action = workflows[rule.action]

    return parts, workflows


if __name__ == '__main__':
    main(sys.argv[1])
