import pytest
import enum
from functools import total_ordering


class Hand(enum.IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSOR = 3


@total_ordering
class Play:
    def __init__(self, shape):
        self.shape = shape

    def __eq__(self, other):
        return self.shape == other.shape

    def __lt__(self, other):
        if self.shape == Hand.ROCK and other.shape == Hand.PAPER:
            return True
        elif self.shape == Hand.PAPER and other.shape == Hand.SCISSOR:
            return True
        elif self.shape == Hand.SCISSOR and other.shape == Hand.ROCK:
            return True
        else:
            return False

        



mapping = {('A', 'X'):Hand.ROCK, ('B', 'Y'):Hand.PAPER, ('C', 'Z'):Hand.SCISSOR}
mapping = {key:value for keys, value in mapping.items() for key in keys}
print(mapping)


def play(me, opponent):
    if me == opponent:
        return me.shape.value + 3
    elif me> opponent:
        return me.shape.value + 6
    else:
        return me.shape.value


def total_score(data):
    return sum(play(Play(mapping[me]), Play(mapping[opponent])) for opponent, me in data)


def read_input(fname):
    with open(fname) as f:
        return [item.split() for item in f.read().splitlines()]


@pytest.fixture()
def sample_input1():
    data = """A Y
B X
C Z"""
    return [item.split(' ') for item in data.splitlines()]

def test_day02_1(sample_input1):
    assert total_score(sample_input1) == 15

data = read_input('./advent2022/day02/input02.txt')
print(data)
print(total_score(data))