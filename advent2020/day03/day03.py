'''https://adventofcode.com/2020/day/3'''


from operator import mul
from functools import reduce

def count_trees(right, down):
    with open('./advent2020/day03/map.txt') as f:
        trees = 0
        line = next(f)
        width = len(line.strip())
        pos = 0
        while True:
            for _ in range(down):
                try:
                    line = next(f)
                except StopIteration:
                    return trees
            line = line.strip()
            if line:
                pos = (pos + right) % width
                if line[pos] == '#':
                    trees += 1


#part1
print(f'Part 1 answer: {count_trees(3, 1)}') # correct answer 173

# part2
slopes = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
all_trees = [count_trees(*slope) for slope in slopes]
print(f'Part 2 answer: {reduce(mul, all_trees, 1)}') # correct answer 4385176320