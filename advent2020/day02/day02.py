'''https://adventofcode.com/2020/day/2'''

part1 = 0
part2 = 0
with open('./advent2020/day02/passwords.txt') as f:
    for line in f:
        line = line.strip()
        if line:
            policy, password = line.strip().split(':')
            limits, char = policy.split(' ')
            lbound, ubound = [int(x) for x in limits.split('-')]
            if not (lbound <= password.count(char) <= ubound):
                part1 += 1
            if sum(password[idx] == char for idx in (lbound, ubound)) == 1: # password starts with space, no need to re-base lbound and ubound
                part2 += 1

# part1
print(f'Part 1 answer: {part1}') # correct answer 500

# part2
print(f'Part 2 answer: {part2}') # correct answer 487