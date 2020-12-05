'''https://adventofcode.com/2020/day/5'''

test_data = {'BFFFBBFRRR':{'row':70, 'column':7, 'seatID':567}, 
             'FFFBBBFRRR':{'row':14, 'column':7, 'seatID':119}, 
             'BBFFBBFRLL':{'row':102, 'column':4, 'seatID':820}}


def get_row(boarding_pass):
    return int(''.join('1' if char == 'B' else '0' for char in boarding_pass[:7]), base=2)


def get_column(boarding_pass):
    return int(''.join('1' if char == 'R' else '0' for char in boarding_pass[-3:]), base=2)


def calc_seatid(boarding_pass):
    return get_row(boarding_pass) * 8 + get_column(boarding_pass)


def test():
    for boarding_pass, value in test_data.items():
        assert value['row'] == get_row(boarding_pass)
        assert value['column'] == get_column(boarding_pass)
        assert value['seatID'] == calc_seatid(boarding_pass)


test()

with open('./advent2020/day05/pass.txt') as f:
    all_seats = [calc_seatid(boarding_pass) for boarding_pass in f.read().splitlines()]
    max_seatid = max(all_seats)


print(f'Part 1 answer: {max_seatid}') # correct answer 928


for seatid in range(max_seatid +1):
    if seatid not in all_seats and seatid + 1 in all_seats and seatid - 1 in all_seats:
        print(f'Part 2 answer: {seatid}') # correct answer 610
