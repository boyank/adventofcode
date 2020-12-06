'''https://adventofcode.com/2020/day/6'''

def answers(myinput):
    for group in myinput.split('\n\n'):
        yield [set(ans) for ans in group.splitlines()]


def count_questions(group):
    return len(set.union(*group))


def common_answers(group):
    return len(set.intersection(*group))


def part1(fname):
    with open(fname) as f:
        return sum(count_questions(group) for group in answers(f.read()))


def part2(fname):
    with open(fname) as f:
        return sum(common_answers(group) for group in answers(f.read()))


def test():
    test_data = """abc

a
b
c

ab
ac

a
a
a
a

b"""


    assert [count_questions(group) for group in answers(test_data)] == [3, 3, 3, 1, 1]
    assert [common_answers(group) for group in answers(test_data)] == [3, 0, 1, 1, 1]


    
if __name__ == '__main__':
    test()
    fname = './advent2020/day06/input.txt'
    result = part1(fname)
    print(f'Part1: {result}') # 6947
    result = part2(fname)
    print(f'Part2: {result}') # 3398