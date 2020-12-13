'''https://adventofcode.com/2020/day/13'''


from pathlib import Path

FNAME = Path(__file__).with_name('input.txt')


def part1(my_time, shuttles):
    shuttle = sorted(shuttles, key=lambda x: my_time % x)[-1]
    depart = my_time % shuttle
    return shuttle * (shuttle - depart)
    

def get_data(fname, keepx=False):
    with fname.open() as f:
        my_time = int(next(f))
        shuttles = next(f).split(',')
        if keepx:
            shuttles = [int(sh) if sh != 'x' else 0 for sh in shuttles if sh != 'x']
        else:
            shuttles = (int(sh) for sh in shuttles if sh != 'x')
        return my_time, shuttles


def test_part_1():
    my_time = 939
    shuttles = 7, 13, 59, 31, 19
    assert part1(my_time, shuttles) == 295


if __name__ == '__main__':
    my_time, shuttles = get_data(FNAME)
    print(f'Part1: {part1(my_time, shuttles)}')
