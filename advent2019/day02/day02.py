'''https://adventofcode.com/2019/day/2'''

import itertools


def intcode(sequence, pointer=0):
    while True:
        opcode = sequence[pointer]
        if opcode == 99:
            return sequence
        else:
            param1, param2, param3 = sequence[pointer + 1:pointer + 4]
            num1 = sequence[param1]
            num2 = sequence[param2]
            if opcode == 1:
                sequence[param3] = num1 + num2
            elif opcode == 2:
                sequence[param3] = num1 * num2
            pointer += 4


def test():
    test_data = [([1,0,0,0,99], [2,0,0,0,99]),
                ([2,3,0,3,99], [2,3,0,6,99]),
                ([2,4,4,5,99,0], [2,4,4,5,99,9801]),
                ([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99])]

    for inp, out in test_data:
        assert intcode(inp) == out


def part1(noun, verb):
    with open('./advent2019/day02/input.txt') as f:
        sequence = [int(num) for num in f.read().split(',')]
        sequence[1] = noun
        sequence[2] = verb
        return intcode(sequence)[0]


def part2():
    for noun, verb in itertools.product(range(100), repeat=2):
        if part1(noun, verb) == 19690720:
            return noun, verb


if __name__ == '__main__':
    test()
    answer = part1(12, 2)
    print(f'Part 1: {answer}') # 3516593
    noun, verb = part2()
    print(f'Part 2: {noun * 100 + verb}') # 7749