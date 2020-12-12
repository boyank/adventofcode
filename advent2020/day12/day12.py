'''https://adventofcode.com/2020/day/12'''

import logging
import pytest
from pathlib import Path
from enum import Enum
from dataclasses import dataclass

logging.basicConfig(level=logging.DEBUG)

FNAME = Path(__file__).with_name('input.txt')

class CP(Enum):
    '''Enumeration for Cardinal Points.
    
    '''
    N = (0, 0, 1)
    E = (90, 1, 0)
    S = (180, 0, -1)
    W = (270, -1, 0)

    def __init__(self, azimuth, xoff, yoff):
        self.azm = azimuth
        self.xoff = xoff
        self.yoff = yoff


@dataclass
class Ship:
    x: int = 0
    y: int = 0
    dir: CP = CP.E


    def move(self, instruction):
        lookup = {0:CP.N, 90:CP.E, 180:CP.S, 270:CP.W}
        cmd = instruction[0]
        steps = int(instruction[1:])
        if cmd == 'R':
            self.dir = lookup[(self.dir.azm + steps) % 360]
        elif cmd == 'L':
            self.dir = lookup[(self.dir.azm - steps) % 360]
        elif cmd == 'F':
            self.x += self.dir.xoff * steps
            self.y += self.dir.yoff * steps
        else:
            cmd = CP.__members__[cmd]
            self.x += cmd.xoff * steps
            self.y += cmd.yoff * steps
        logging.debug(self)


    def mdiff(self):
        return abs(self.x) + abs(self.y)


def get_data(fname):
    with fname.open() as f:
        return f.read().splitlines()

def part1():
    ship = Ship()
    for move in get_data(FNAME):
        ship.move(move)
    return ship.mdiff()


@pytest.fixture
def input_data():
    return 'F10,N3,F7,R90,F11'


@pytest.mark.usefixtures('input_data')
def test_ship_move(input_data):
    ship = Ship()
    for move in input_data.split(','):
        ship.move(move)
    assert ship.mdiff() == 25


if __name__ == '__main__':

    print(f"The Manhattan distance between that location and the ship's starting position {part1()}")
