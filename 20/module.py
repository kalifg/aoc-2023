import collections
from enum import Enum
from typing import List


class Pulse(Enum):
    NONE = -1
    LOW = 0
    HIGH = 1

    def __repr__(self):
        return self.name

    def __bool__(self):
        return self == Pulse.HIGH


class State(Enum):
    OFF = False
    ON = True


class Signal:
    def __init__(self, source: 'Module', destination: 'Module', pulse: Pulse):
        self.source = source
        self.destination = destination
        self.pulse = pulse

    def __repr__(self):
        return f'<{self.source.symbol}{self.source.name} ({repr(self.pulse)})-> {self.destination.symbol}{self.destination.name}>'


class Module:
    def __init__(self, name: str):
        self.name = name
        self.symbol = '?'
        self.sources: List[Module] = []
        self.destinations: List[Module] = []

    def process_pulse(self, source: 'Module', input: Pulse, signal_queue: collections.deque):
        for destination in self.destinations:
            output = self.generate_pulse(source, input, destination)

            if output is not None:
                signal_queue.append(Signal(self, destination, output))

    def generate_pulse(self, source: 'Module', input: Pulse, destination: 'Module') -> Pulse | None:
        return None

    def __repr__(self):
        return f'<Module: {self.name}({self.__class__.__name__}), Destinations: {[destination.name for destination in self.destinations]}>'


class Broadcaster(Module):
    def __init__(self, name: str):
        super().__init__(name)
        self.symbol = ''

    def generate_pulse(self, source: Module, input: Pulse, destination: 'Module') -> Pulse | None:
        return input


class FlipFlop(Module):
    def __init__(self, name: str):
        super().__init__(name)
        self.symbol = '%'
        self.state = False

    def process_pulse(self, source: 'Module', input: Pulse, signal_queue: collections.deque):
        if input == Pulse.LOW:
            self.state = not self.state

        super().process_pulse(source, input, signal_queue)

    def generate_pulse(self, source: Module, input: Pulse, destination: 'Module') -> Pulse | None:
        if input == Pulse.LOW:
            return Pulse.HIGH if self.state else Pulse.LOW

        return None


class Conjunction(Module):
    def __init__(self, name: str):
        super().__init__(name)

        self.symbol = '&'
        self.last_pulses = None

    def generate_pulse(self, source: 'Module', input: Pulse, destination: 'Module') -> Pulse | None:
        if not self.last_pulses:
            self.last_pulses = {source: Pulse.LOW for source in self.sources}

        self.last_pulses[source] = input

        return Pulse.LOW if all(self.last_pulses.values()) else Pulse.HIGH


class Button(Module):
    def __init__(self, name: str):
        super().__init__(name)
        self.symbol = ''

    def push(self, signal_queue: collections.deque):
        self.process_pulse(None, Pulse.NONE, signal_queue)

    def generate_pulse(self, source: Module, input: Pulse, destination: 'Module'):
        return Pulse.LOW



