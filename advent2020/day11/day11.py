'''https://adventofcode.com/2020/day/11'''

import pytest
from pathlib import Path
from collections import Counter
import logging
from pprint import pprint

FNAME = Path(__file__).with_name('input.txt')
FNAME_TEST = Path(__file__).with_name('test_input.txt')


def get_data(fname):
    with fname.open() as f:
        data = f.read().split ('\n\n')
        for plan in data:
            yield plan.splitlines()


def do_round(plan, crowd=3, level=1):
    next_plan = []
    for rowid, row in enumerate(plan):
        next_plan.append([])
        for colid, seat in enumerate(row):
            logging.debug(f'[{rowid}, {colid}]: {seat}')
            if seat != '.':
                occupied_seats = check_occupied(plan, rowid, colid, level=level)
                if seat == 'L' and not occupied_seats:
                    next_plan[-1].append('#')
                elif seat == '#' and occupied_seats > crowd:
                    next_plan[-1].append('L')
                else:
                    next_plan[-1].append(seat)
            else:
                next_plan[-1].append('.')
            logging.debug(f'[{rowid}, {colid}] :: {occupied_seats} :: {next_plan[rowid][colid]}')

    next_plan = [''.join(row) for row in next_plan]
    return next_plan


def process(plan, crowd=3, level=1):
    num_rows = len(plan)
    num_cols = len(plan[0])
    plans = ['\n'.join(plan)]
    plan = [list(row) for row in plan]
    while True:
        plan = do_round(plan, crowd=crowd, level=level)
        logging.debug(plan)
        if plan in plans:
            return Counter('\n'.join(plans[-1]))['#']
        plans.append(plan)


def check_row(plan, row, col, numrows, numcols, level):
    seats = 0
    offsets =  {'LC':(-1, -1), 
                'RC':(1, numcols)}
    for co, limit in offsets.values():
        for idx, colid in enumerate(range(col + co, limit, co), start=1):
            seat = plan[row][colid]
            if seat == '#':
                seats += 1
            if seat != '.' or idx == level:
                break
    return seats


def check_col(plan, row, col, numrows, numcols, level):
    seats = 0
    offsets =  {'TC':(-1, -1), 
                'DC':(1, numrows)}
    for ro, limit in offsets.values():
        for idx, rowid in enumerate(range(row + ro, limit, ro), start=1):
            seat = plan[rowid][col]
            if seat == '#':
                seats += 1
            if seat != '.' or idx == level:
                break
    return seats


def check_diagonals(plan, row, col, numrows, numcols, level):
    seats = 0
    offsets = {'TL':(-1, -1, -1, -1), 
               'TR':(-1, 1, -1, numcols), 
               'DL':(1, -1, numrows, -1), 
               'DR':(1, 1, numrows, numcols)}
    for key, (ro, co, rlimit, climit) in offsets.items():
        break_out = False
        for ridx, rowid in enumerate(range(row + ro, rlimit, ro), start=1):
            for cidx, colid in enumerate(range(col + co, climit, co), start=1):
                if ridx == cidx:
                    seat = plan[rowid][colid]
                    if seat == '#':
                        seats += 1
                    if seat != '.' or (cidx == level):
                        break_out = True
            if break_out:
                break
    return seats


def check_occupied(plan, row, col, level):
    numrows = len(plan)
    numcols = len(plan[0])
    seats = 0
    seats += check_row(plan, row, col, numrows, numcols, level)
    seats += check_col(plan, row, col, numrows, numcols, level)
    seats += check_diagonals(plan, row, col, numrows, numcols, level)
    return seats


def part1():
    data = get_data(FNAME)
    plan = next(data)
    return process(plan, crowd=3, level=1)


def part2():
    data = get_data(FNAME)
    plan = next(data)
    return process(plan, crowd=4, level=0)



@pytest.fixture
def input_data():
    data = get_data(FNAME_TEST)
    data = list(data)
    return zip(data[:-1], data[1:])


@pytest.fixture
def input_data2():
    data = get_data(FNAME_TEST.with_name('test_input2.txt'))
    return next(data)
    

@pytest.mark.usefixtures('input_data')
def test_get_data(input_data):
    data, expected = next(input_data)
    expected = ['L.LL.LL.LL', 'LLLLLLL.LL', 'L.L.L..L..',
                'LLLL.LL.LL', 'L.LL.LL.LL', 'L.LLLLL.LL',
                '..L.L.....', 'LLLLLLLLLL', 'L.LLLLLL.L',
                'L.LLLLL.LL']
    assert data == expected


@pytest.mark.usefixtures('input_data')
def test_do_round(input_data):
    for plan, expected in input_data:
        plan = [list(row) for row in plan]
        assert do_round(plan) == expected


@pytest.mark.usefixtures('input_data')
def test_count(input_data):
    data = get_data(FNAME_TEST)
    plan = next(data)
    assert process(plan) == 37


@pytest.mark.usefixtures('input_data2')
def test_check_cols_l1(input_data2):
    assert check_col(input_data2, 1, 2, len(input_data2), len(input_data2[0]), level=1) == 0


@pytest.mark.usefixtures('input_data2')
def test_check_rows_l1(input_data2):
    assert check_row(input_data2, 1, 2, len(input_data2), len(input_data2[0]), level=1) == 1


@pytest.mark.usefixtures('input_data2')
def test_check_diagonals_l1(input_data2):
    assert check_diagonals(input_data2, 1, 2, len(input_data2), len(input_data2[0]), level=1) == 1


@pytest.mark.usefixtures('input_data2')
def test_check_cols(input_data2):
    assert check_col(input_data2, 4, 3, len(input_data2), len(input_data2[0]), level=0) == 2


@pytest.mark.usefixtures('input_data2')
def test_check_rows(input_data2):
    assert check_row(input_data2, 4, 3, len(input_data2), len(input_data2[0]), level=0) == 2


@pytest.mark.usefixtures('input_data2')
def test_check_diagonals(input_data2):
    assert check_diagonals(input_data2, 4, 3, len(input_data2), len(input_data2[0]), level=0) == 4


def test_check_cols3():
    data = get_data(FNAME_TEST)
    next(data)
    plan = next(data)
    assert check_col(plan, 0, 6, len(plan), len(plan), level=0) == 1


def test_check_rows3():
    data = get_data(FNAME_TEST)
    next(data)
    plan = next(data)
    assert check_row(plan, 0, 0, len(plan), len(plan), level=0) == 1


def test_check_diagonals3():
    data = get_data(FNAME_TEST)
    next(data)
    plan = next(data)
    assert check_diagonals(plan, 0, 0, len(plan), len(plan), level=0) == 1


@pytest.mark.usefixtures('input_data2')
def test_check_occupied(input_data2):
    assert check_occupied(input_data2, 4, 3, level=0) == 8


def test_do_round_level0():
    data = get_data(FNAME_TEST)
    plan = next(data)
    assert process(plan, crowd=4, level=0) == 26


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(f'part1: {part1()}')
    print(f'part2: {part2()}')
