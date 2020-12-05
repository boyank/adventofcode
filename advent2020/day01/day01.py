'''https://adventofcode.com/2020/day/1'''

from itertools import combinations
from operator import mul
from functools import reduce
with open('./advent2020/day01/numbers.txt') as f:
    numbers = [int(line) for line in f if line.strip()]


def find_numbers(numbers, nums, target=2020):
    for comb in combinations(numbers, nums):
        if sum(comb) == target:
            return comb, reduce(mul, comb, 1)

# part1
comb, answer = find_numbers(numbers, 2)
print(f'Part 1 answer: {answer}') # correct answer 270144

# part2
comb, answer = find_numbers(numbers, 3)
print(f'Part 2 answer: {answer}') # correct answer 261342720