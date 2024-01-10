import collections
from typing import List, Dict

import np
import numpy
import sympy

import module
import sys

from shared import input


last_pulses_cache: Dict[str, set]
last_pulses_cache = {}


# 944750144 is right
#
# 11025596 is too low
# 55637976377 is too low
# 881418406106957723406690 is too high
# 222718819437131 is right (Chinese remainder theorem)
def main(filename: str):
    lines = input.readfile(filename)

    module_definitions = []

    for line in lines:
        name, destinations = line.split(' -> ')
        t, name = split_module_definition(name)
        destinations = destinations.split(', ')

        module_definitions.append((t, name, destinations))

    print(module_definitions)

    modules = create_modules(module_definitions)
    print(modules)
    print()

    total_pulses = push_button(modules, 8010)

    column = 0
    syms = []
    coefficients = []
    constants = []

    for key, pushes in last_pulses_cache.items():
        pushes = sorted(list(pushes))
        differential = pushes[1] - pushes[0]

        print(f'{key}: {pushes}: {differential}')
        coefficients.append(differential)
        constants.append(pushes[0])
        syms.append(f'a{column}')

        column += 1

    print(constants)

    syms = sympy.symbols(syms, integer=True)
    equation = 0

    for c, s in zip(coefficients, syms):
        if not equation:
            equation += c * s
        else:
            equation -= c * s

    constant = constants[0]
    constant -= sum(constants[1:])
    equation += constant

    print(equation)

    solution = sympy.diophantine(equation)
    print(solution)

    a, b, c, d = sympy.symbols('a b c d')
    a, b, c, d = solution.pop()

    t_0, t_1, t_2 = sympy.symbols("t_0 t_1 t_2", integer=True)
    lq, dl, hb, hf = sympy.symbols('lq dl hb hf')

    lq = 3738 + 3739 * a
    dl = 3796 + 3797 * b
    hb = 3918 + 3919 * c
    hf = 4002 + 4003 * d

    for t0 in range(2):
        for t1 in range(2):
            for t2 in range(2):
                lq0 = lq.subs({t_0: t0})
                dl0 = dl.subs({t_0: t0, t_1: t1})
                hb0 = hb.subs({t_0: t0, t_1: t1, t_2: t2})
                hf0 = hf.subs({t_0: t0, t_1: t1, t_2: t2})

                print(lq0, dl0, hb0, hf0)

    #
    # substituted_solution = solution.subs({t_0: 0, t_1: 0, t_2: 0})
    #
    # print(substituted_solution)

    # for solution in solutions:
    #     for var in solution:
    #         print(var, type(var))
    #         val = var.subs(t_0, 0)
    #         print(val)




    # matrix = numpy.array(matrix)
    # constants = numpy.array(constants)
    #
    # print(matrix)
    # print(constants)
    #
    # solution = numpy.linalg.solve(matrix, constants)


    # print(f'Total pulses: {total_pulses}')
    # print(f'Answer: {total_pulses[module.Pulse.LOW] * total_pulses[module.Pulse.HIGH]}')


def push_button(modules: List[module.Module], times: int = 1, verbose: bool = False):
    signal_queue = collections.deque()
    total_pulses = {module.Pulse.LOW: 0, module.Pulse.HIGH: 0}

    for i in range(times):
        modules['button'].push(signal_queue)

        while signal_queue:
            signal: module.Signal = signal_queue.popleft()

            if verbose:
                print(signal)

            # if signal.destination.name == 'rx' and signal.pulse == module.Pulse.LOW:
            if signal.destination.name in ['hb', 'hf', 'dl', 'lq']:
                signal.destination: module.Conjunction

                if signal.destination.last_pulses:
                    last_pulses = {m.name: pulse for m, pulse in signal.destination.last_pulses.items()}
                    if all([pulse.name == 'HIGH' for pulse in last_pulses.values()]):
                        # print(f"{i}: {last_pulses}")
                        if signal.destination.name not in last_pulses_cache.keys():
                            last_pulses_cache[signal.destination.name] = set()

                        last_pulses_cache[signal.destination.name].add(i)

                # print(f'{signal.pulse} detected being sent to module {signal.destination} on push {i}')
                # return

            total_pulses[signal.pulse] += 1
            signal.destination.process_pulse(signal.source, signal.pulse, signal_queue)

        if verbose:
            print()

    return total_pulses


def create_modules(module_definitions):
    modules = {'button': module.Button('button')}

    for type, name, _ in module_definitions:
        match type:
            case 'broadcaster':
                module_class = module.Broadcaster
            case '%':
                module_class = module.FlipFlop
            case '&':
                module_class = module.Conjunction
            case _:
                raise ValueError(f'Unknown module type {type}')

        modules[name] = module_class(name)

    for _, name, destinations in module_definitions:
        for destination in destinations:
            if destination not in modules.keys():
                modules[destination] = module.Module(destination)

            modules[name].destinations.append(modules[destination])
            modules[destination].sources.append(modules[name])

    modules['button'].destinations.append(modules['broadcaster'])
    return modules


def split_module_definition(definition: str) -> (str, str):
    return ('broadcaster', 'broadcaster') if definition == 'broadcaster' else (definition[0], definition[1:])


if __name__ == '__main__':
    main(sys.argv[1])
