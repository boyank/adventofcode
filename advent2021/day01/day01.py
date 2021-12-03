import pytest


def get_data(fname):
    with open(fname) as f:
        return [int(num) for num in f.read().splitlines()]


def part1(data):
    return sum(item1 < item2 for item1, item2 in zip(data[:-1], data[1:]))

def part2(data, shift):
    return sum(item < data[idx + shift] for idx, item in enumerate(data[:-shift]))

@pytest.fixture()
def input_data():
    fname = './advent2021/day01/test_input.txt'
    return get_data(fname)


@pytest.mark.usefixtures('input_data')
def test_part1(input_data):
    assert part1(input_data) == 7


# @pytest.mark.usefixtures('input_data')
# def test_part2(input_data):
#     assert part2(input_data, 127) == 62


def test_get_data():
    fname = './advent2021/day01/test_input.txt'
    expected = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    assert get_data(fname) == expected


if __name__ == '__main__':
    fname = './advent2021/day01/input.txt'
    data = get_data(fname)
    result = part1(data)
    print(f'{result} measurements are larger than the previous measurement.') # 1692
    result = part2(data, 3)
    print(f'{result} sums are larger than the previous sum') # 67587168