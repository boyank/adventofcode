'''https://adventofcode.com/2020/day/15'''

from collections import deque

def part1(my_input, limit):
    n = len(my_input)
    nums = {number:deque((idx, idx), maxlen=2) for number, idx in zip(my_input, range(1, n+1))}
    number = my_input[-1]
    while n < limit:
        n += 1
        n1, n2 = nums[number]
        number = n2 - n1
        nums.setdefault(number, deque((n, n), maxlen=2)).append(n)
    return number

def test_part1():
    data = [((1, 3, 2), 1), ((2, 1, 3), 10), ((1, 2, 3), 27),
            ((2, 3, 1), 78), ((3, 2, 1), 438), ((3, 1, 2), 1836)]
    for my_input, expected in data:
        assert part1(my_input) == expected

if __name__ == '__main__':
    my_input = 6,13,1,15,2,0
    print(f'2020th number: {part1(my_input, 2020)}') # 1194
    print(f'30000000th number: {part1(my_input, 30000000)}') # 48710

