'''https://adventofcode.com/2020/day/9#part2'''

import pytest
from itertools import combinations
from collections import deque


def get_data(fname):
    with open(fname) as f:
        return [int(num) for num in f.read().splitlines()]


def part1(data, length):
    preamble = deque(data[:length],  maxlen=length)
    for num in data[length:]:
        if all(num != sum(item) for item in combinations(preamble, 2)):
            return num
        else:
            preamble.append(num)


def part2(data, number):
    idx = data.index(number)
    for length in range(2, idx):
        terms = deque(data[:length-1], maxlen=length)
        for num in data[length-1:idx]:
            terms.append(num)
            if sum(terms) == number:
                return min(terms) + max(terms)
        

@pytest.fixture()
def input_data():
    with open('./advent2020/day09/test_input.txt') as f:
        return [int(num) for num in f.read().splitlines()]


@pytest.mark.usefixtures('input_data')
def test_part1(input_data):
    assert part1(input_data, 5) == 127



@pytest.mark.usefixtures('input_data')
def test_part2(input_data):
    assert part2(input_data, 127) == 62


def test_get_data():
    fname = './advent2020/day09/test_input.txt'
    expected = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 
                117, 150, 182, 127, 219, 299, 277, 309, 576]
    assert get_data(fname) == expected


def test_aoc():
    fname = './advent2020/day09/input.txt'
    data = get_data(fname)
    result = part1(data, 25)
    assert result == 400480901
    result = part2(data, result)
    assert result == 67587168


if __name__ == '__main__':
    fname = './advent2020/day09/input.txt'
    with open(fname) as f:
        data = [int(num) for num in f.read().splitlines()]
    result = part1(data, 25)
    print(f'First number that does not have this property: {result}') # 400480901
    result = part2(data, result)
    print(f'The encryption weakness in your XMAS-encrypted list of numbers: {result}') # 67587168