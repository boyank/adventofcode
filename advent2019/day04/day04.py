'''https://adventofcode.com/2019/day/4'''

from more_itertools import run_length

def check(number):
    number = str(number)
    pairs = list(zip(number[:-1], number[1:]))
    return all(num2 >= num1 for num1, num2 in pairs) and any(num1==num2 for num1, num2 in pairs)


def check2(number):
    number = str(number)
    pairs = list(zip(number[:-1], number[1:]))
    return all(num2 >= num1 for num1, num2 in pairs) and any(counter == 2 for num, counter in run_length.encode(number))


def part1():
    '''input 256310-732736'''

    start = 256310
    end = 732736
    return sum(check(number) for number in range(start, end+1))

def part2():
    '''input 256310-732736'''

    start = 256310
    end = 732736
    return sum(check2(number) for number in range(start, end+1))


def test():
    test_data = [(111111,True), (223450, False), (123789, False)]
    for number, expect in test_data:
        assert check(number) == expect

def test_part2():
    test_data = [(112233,True), (1234444, False), (111122, True)]
    for number, expect in test_data:
        assert check2(number) == expect


if __name__ == '__main__':
    test()
    test_part2()
    print(f'Part 1: {part1()}')
    print(f'Part 2: {part2()}')