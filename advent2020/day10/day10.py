'''https://adventofcode.com/2020/day/10'''

import pytest
from pathlib import Path
from collections import Counter


FNAME = Path(__file__).with_name('input.txt')


def get_data(fname):
    with fname.open() as f:
        return [int(num) for num in f] 


def check_adapters(data):
    data = list(data)
    data.append(0)
    data.sort()
    data.append(data[-1] + 3)
    cntr = Counter(device2 - device1 for device1, device2 in zip(data[:-1], data[1:]))
    return cntr


def possible_connections(data):
    data.append(0)
    data.sort(reverse=True)
    all_connections = [1]
    for idx, adapter in enumerate(data[1:], start=1):
        connections = 0
        for offset in (1, 2, 3):
            prev_idx = idx - offset
            if prev_idx >= 0:
                if 1 <= data[prev_idx] - adapter <= 3:
                    connections += all_connections[prev_idx]
        all_connections.append(connections)
    return all_connections[-1]
    
    
def part1():
    data = get_data(FNAME)
    cntr = check_adapters(data)
    return cntr[1] * cntr[3]


def part2():
    data = get_data(FNAME)
    return possible_connections(data)


@pytest.fixture
def input_data():
    return [([16, 10, 15, 5, 1,
              11, 7, 19, 6, 12, 4], {'part1':35, 'part2':8}),

            ([28, 33, 18, 42, 31, 14, 
              46, 20, 48, 47, 24, 23, 
              49, 45, 19, 38, 39, 11,
              1, 32, 25, 35, 8, 17, 7, 
              9, 4, 2, 34, 10, 3], {'part1':220, 'part2':19208})]


@pytest.mark.usefixtures('input_data')
def test_adapter_diff(input_data):
    for data, expected in input_data:
        cntr = check_adapters(data)
        assert cntr[1] * cntr[3] == expected['part1']


@pytest.mark.usefixtures('input_data')
def test_chain(input_data):
    for data, expected in input_data:
        assert possible_connections(data) == expected['part2']

if __name__ == '__main__':
    print(f'part1: {part1()}')
    print(f'part2: {part2()}')