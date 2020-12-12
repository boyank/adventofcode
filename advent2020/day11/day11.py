'''https://adventofcode.com/2020/day/11'''

from pathlib import Path
from collections import Counter
import logging

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


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(f'part1: {part1()}')
    print(f'part2: {part2()}')
