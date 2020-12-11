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


def process(plan):
    num_rows = len(plan)
    num_cols = len(plan[0])
    plans = ['\n'.join(plan)]
    plan = [list(row) for row in plan]
    while True:
        plan = do_round(plan)
        logging.debug(plan)
        if plan in plans:
            return Counter('\n'.join(plans[-1]))['#']
        plans.append(plan)


def num_occupied(plan, row, col):
    numrows = len(plan)
    numcols = len(plan[0])
    prev_row = row - 1
    next_row = row + 1
    prev_col = col - 1
    next_col = col + 1
    seats = []
    if prev_row >= 0:
        if prev_col >= 0:
            seats.append(plan[prev_row][prev_col])
        seats.append(plan[prev_row][col])
        if next_col < numcols:
            seats.append(plan[prev_row][next_col])
    if prev_col >= 0:
        seats.append(plan[row][prev_col])
    if next_col < numcols:
        seats.append(plan[row][next_col])
    if next_row < numrows:
        if prev_col >= 0:
            seats.append(plan[next_row][prev_col])
        seats.append(plan[next_row][col])
        if next_col < numcols:
            seats.append(plan[next_row][next_col])
    return Counter(seats)['#']


def check_row(plan, row, col, numrows, numcols, level):
    seats = []
    offsets =  {'LC':(-1, 0), 
                'RC':(1, numcols)}
    for co, limit in offsets.values():
        for idx, colid in enumerate(range(col + co, limit, co), start=1):
            seat = plan[row][colid]
            seats.append(seat)
            if seat != '.' or idx == level:
                break
    return seats


def check_col(plan, row, col, numrows, numcols, level):
    seats = []
    offsets =  {'TC':(-1, 0), 
                'DC':(1, numrows)}
    for ro, limit in offsets.values():
        for idx, rowid in enumerate(range(row + ro, limit, ro), start=1):
            seat = plan[rowid][col]
            seats.append(seat)
            if seat != '.' or idx == level:
                break
    return seats


def check_diagonals(plan, row, col, numrows, numcols, level):
    seats = []
    offsets = {'TL':(-1, -1, 0, 0), 
               'TR':(-1, 1, 0, numcols), 
               'DL':(1, -1, numrows, 0), 
               'DR':(1, 1, numrows, numcols)}
    for ro, co, rlimit, climit in offsets.values():
        for ridx, rowid in enumerate(range(row + ro, rlimit, ro), start=1):
            for cidx, colid in enumerate(range(col + co, climit, co), start=1):
                seat = plan[rowid][colid]
                seats.append(seat)
                if seat != '.' or cidx == level:
                    break
            if ridx == level:
                break
    return seats

def check_occupied(plan, row, col, level):
    numrows = len(plan)
    numcols = len(plan[0])
    seats = []
    seats.extend(check_row(plan, row, col, numrows, numcols, level))
    seats.extend(check_col(plan, row, col, numrows, numcols, level))
    seats.extend(check_diagonals(plan, row, col, numrows, numcols, level))
    return Counter(seats)['#']


def part1():
    data = get_data(FNAME)
    plan = next(data)
    return process(plan)



@pytest.fixture
def input_data():
    data = get_data(FNAME_TEST)
    data = list(data)
    return zip(data[:-1], data[1:])
    


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
    return process(plan) == 37


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(f'part1: {part1()}')
    # print(f'part2: {part2()}')
    pass