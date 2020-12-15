'''https://adventofcode.com/2020/day/15'''

from collections import deque

def part1(my_input):
    n = len(my_input)
    nums = {number:deque((idx, idx), maxlen=2) for number, idx in zip(my_input, range(1, n+1))}
    number = my_input[-1]
    while n < 2020:
        n += 1
        prev = nums.setdefault(number, deque((n, n), maxlen=2))
        n1, n2 = prev
        new_number = n2 - n1
        nums.setdefault(new_number, deque((n, n), maxlen=2)).append(n)
        number = new_number
    return number

def test_part1():
    data = [((1, 3, 2), 1), ((2, 1, 3), 10), ((1, 2, 3), 27),
            ((2, 3, 1), 78), ((3, 2, 1), 438), ((3, 1, 2), 1836)]
    for my_input, expected in data:
        assert part1(my_input) == expected

if __name__ == '__main__':
    my_input = 6,13,1,15,2,0
    print(f'Part1: {part1(my_input)}')


