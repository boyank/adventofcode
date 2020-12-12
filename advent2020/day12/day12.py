'''https://adventofcode.com/2020/day/12'''

import logging
import pytest
from pathlib import Path
from enum import Enum
from dataclasses import dataclass
from operator import add, sub

logging.basicConfig(level=logging.INFO)

FNAME = Path(__file__).with_name('input.txt')

class CP(Enum):
    '''Enumeration for Cardinal Points.
    
    '''

    N = (0, 0, 1)
    E = (90, 1, 0)
    S = (180, 0, -1)
    W = (270, -1, 0)
    NE = (0, 1, 1)
    SE = (90, 1, -1)
    SW = (180, -1, -1)
    NW = (270, -1, +1)


    def __init__(self, azimuth, xoff, yoff):
        self.azm = azimuth
        self.xoff = xoff
        self.yoff = yoff


@dataclass
class Waypoint:
    relx: int
    rely: int

    @property
    def quadrant(self):
        return {
        (True, True):CP.NE,
        (True, False):CP.SE,
        (False, False):CP.SW,
        (False, True):CP.NW} [(self.relx >= 0, self.rely >= 0)]

    def __repr__(self):
        return f'{self.relx}, {self.rely}, {self.quadrant}'


@dataclass
class Ship:
    x: int = 0
    y: int = 0
    orientation: CP = CP.E
    vector: Waypoint = Waypoint(1, 0)

    def move(self, instruction, moving_wpt=True):
        wpt_lookup = {0:CP.NE, 90:CP.SE, 180:CP.SW, 270:CP.NW}
        ship_lookup = {0:CP.N, 90:CP.E, 180:CP.S, 270:CP.W}
        cmd = instruction[0]
        steps = int(instruction[1:])
        if cmd in ('R', 'L'):
            op = {'R':add, 'L':sub}[cmd]
            rotation = wpt_lookup[op(self.vector.quadrant.azm, steps) % 360]
            x = abs(self.vector.relx)
            y = abs(self.vector.rely)

            if (steps // 90) % 2:
                x, y = y, x

            self.vector.relx = x * rotation.xoff
            self.vector.rely = y * rotation.yoff
            rotation = op(self.orientation.azm, steps) % 360
            self.orientation = ship_lookup[rotation]
        
        elif cmd == 'F':
            if moving_wpt:
                self.x += self.vector.relx * steps
                self.y += self.vector.rely * steps
            else:
                self.x += self.orientation.xoff * steps
                self.y += self.orientation.yoff * steps
        else:
            if moving_wpt:
                quad = CP.__members__[cmd]
                self.vector.relx += quad.xoff * steps
                self.vector.rely += quad.yoff * steps
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
        ship.move(move, moving_wpt=False)
    return ship.mdiff()


def part2():
    ship = Ship(vector=Waypoint(10, 1))
    for move in get_data(FNAME):
        ship.move(move)
    return ship.mdiff()


@pytest.fixture
def input_data():
    return 'F10,N3,F7,R90,F11'


@pytest.fixture
def myship():
    return Ship(vector=Waypoint(10, 1))


@pytest.mark.usefixtures('input_data')
def test_ship_move(input_data):
    ship = Ship()
    for move in input_data.split(','):
        ship.move(move, moving_wpt=False)
    assert ship.mdiff() == 25


@pytest.mark.usefixtures('input_data')
def test_wpt_move(input_data):
    ship = Ship(vector=Waypoint(10, 1))
    for move in input_data.split(','):
        ship.move(move)
    assert ship.mdiff() == 286


def test_NESW():
    for move, expected in zip('NESW', [(10, 5), (14, 1), (10, -3), (6, 1)]):
        myship = Ship(vector=Waypoint(10, 1))
        myship.move(f'{move}4')
        assert myship.x == 0
        assert myship.y == 0
        assert myship.orientation == CP.E
        assert myship.vector == Waypoint(*expected)


def test_rotation():
    for deg, expected in zip((90, 180, 270), [(CP.S, (1, -10)), (CP.W, (-10, -1)), (CP.N, (-1, 10))]):
        myship = Ship(vector=Waypoint(10, 1))
        myship.move(f'R{deg}')
        assert myship.x == 0
        assert myship.y == 0
        assert myship.orientation == expected[0]
        assert myship.vector == Waypoint(*expected[1])


if __name__ == '__main__':
    print(f"The Manhattan distance between that location and the ship's starting position {part1()}")
    print(f"The Manhattan distance between that location and the ship's starting position {part2()}")