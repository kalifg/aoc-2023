from enum import Enum
from typing import Optional, List, Dict


class PlotType(Enum):
    START = 'S'
    ROCK = '#'
    GARDEN = '.'


class Plot:
    def __init__(self, plot_type: PlotType):
        self.plot_type = plot_type
        self.is_end_point = False

        self.neighbors: Dict[str, Optional[Plot]] = {
            'north': None,
            'south': None,
            'east': None,
            'west': None,
        }

        self.location = None
        self.unique_id = None

    def __repr__(self):
        return f'<{self.unique_id}: {self.location}: {self.plot_type.value}>'

    @property
    def north(self) -> Optional['Plot']:
        return self.neighbors['north']

    @north.setter
    def north(self, plot: 'Plot'):
        self.neighbors['north'] = plot

    @property
    def south(self) -> Optional['Plot']:
        return self.neighbors['south']

    @south.setter
    def south(self, plot: 'Plot'):
        self.neighbors['south'] = plot

    @property
    def east(self) -> Optional['Plot']:
        return self.neighbors['east']

    @east.setter
    def east(self, plot: 'Plot'):
        self.neighbors['east'] = plot

    @property
    def west(self) -> Optional['Plot']:
        return self.neighbors['west']

    @west.setter
    def west(self, plot: 'Plot'):
        self.neighbors['west'] = plot

    @property
    def x(self) -> Optional[int]:
        return None if not self.location else self.location[0]

    @property
    def y(self) -> Optional[int]:
        return None if not self.location else self.location[1]

    @property
    def can_step_on(self):
        return self.plot_type != PlotType.ROCK

    @property
    def elligible_neighbors(self) -> Dict[str, 'Plot']:
        return {direction: neighbor for direction, neighbor in self.neighbors.items() if neighbor and neighbor.can_step_on}

    def reset(self):
        self.is_end_point = False


def reset_plots(plots: List[List[Plot]]):
    for row in plots:
        for plot in row:
            plot.reset()


def print_plots(plots: List[List[Plot]]):
    print()

    for row in plots:
        for plot in row:
            c = 'O' if plot.is_end_point else plot.plot_type.value
            print(c, end='')

        print()

    print()