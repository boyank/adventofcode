'''https://adventofcode.com/2020/day/14'''

import pytest
from pathlib import Path
from itertools import product

FNAME = Path(__file__).with_name('input.txt')
FNAME_TEST = Path(__file__).with_name('test_input.txt')
FNAME_TEST2 = Path(__file__).with_name('test_input2.txt')


def get_masked_addresses(mask):
    for bits in product((0, 1), repeat=mask.count('X')):
        bits = iter(bits)
        yield ''.join(map(str, (next(bits) if m == 'X' else m for m in mask)))


def masked(value, mask, return_int=False):
    value = ''.join(m if m != 'X' else v
                       for m, v in zip(mask, f'{value:0>36b}'))
    if return_int:
        return int(value, base=2)
    return value


def masked2(value, mask):
    bits = []
    return ''.join(v if m == '0' else m
                       for m, v in zip(mask, f'{value:0>36b}'))


def part1(fname):
    memory = {}
    with fname.open() as f:
        for line in f:
            if line.startswith('mask'):
                mask = line.split('=')[-1].strip()
            else:
                address, value = line.strip().split(' = ')
                address = address[4:-1]
                value = int(value)
                memory[address] = masked(value, mask, return_int=True)
    return sum(memory.values())


def part2(fname):
    memory = {}
    with fname.open() as f:
        for line in f:
            if line.startswith('mask'):
                mask = line.split('=')[-1].strip()
            else:
                address, value = line.strip().split(' = ')
                address = masked2(int(address[4:-1]), mask)
                value = int(value)
                addresses = get_masked_addresses(address)
                for address in addresses:
                    memory[address] = value
    return sum(memory.values())


@pytest.fixture
def input_data():
    return ((8, 11, 73), (7, 101, 101), (8, 0, 64))


@pytest.mark.usefixtures('input_data')
def test_masked(input_data):
    mask = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X'
    for address, value, expected in input_data:
        assert masked(value, mask, return_int=True) == expected


@pytest.mark.usefixtures('input_data')
def test_part1(input_data):
    assert part1(FNAME_TEST) == 165


def test_get_masks():
    mask = '000000000000000000000000000000X1001X'
    address = masked2(42, mask)
    assert list(get_masked_addresses(address)) == ['000000000000000000000000000000011010',
                                                   '000000000000000000000000000000011011', 
                                                   '000000000000000000000000000000111010', 
                                                   '000000000000000000000000000000111011']



@pytest.mark.usefixtures('input_data')
def test_part2(input_data):
    assert part2(FNAME_TEST2) == 208


if __name__  == '__main__':
    print(f'Part1: {part1(FNAME)}') # 3059488894985
    print(f'Part2: {part2(FNAME)}') # 2900994392308
