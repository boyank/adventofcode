'''https://adventofcode.com/2019/day/6'''

def count_orbits(objects):
    total_orbits = 0
    for obj1, obj2 in objects.items():
        while True:
            if obj2:
                total_orbits += 1
                obj1, obj2 = obj2, objects[obj2]
            else:
                break
    return total_orbits


def count_orbits2(objects):
    '''An alternative implementation of part1 after completing part2.

    '''

    return sum(len(get_transfers(objects, obj)) for obj in objects)


def get_transfers(objects, start):
    transfers = []
    while True:
        obj = objects[start]
        if obj:
            transfers.append(obj)
            start = obj
        else:
            break
    return transfers


def preprocess(data):
    data = [item.split(')') for item in data.splitlines()]
    objects = {key:None for item in data for key in item}
    for obj1, obj2 in data:
        objects[obj2] = obj1
    return objects


def part1(fname):
    with open(fname) as f:
        data = preprocess(f.read())
    return count_orbits(data)


def part1a(fname):
    with open(fname) as f:
        data = preprocess(f.read())
    return count_orbits2(data)



def part2(fname):
    with open(fname) as f:
        data = preprocess(f.read())
    santa = get_transfers(data, 'SAN')
    for cnt, obj in enumerate(get_transfers(data, 'YOU')):
        if obj in santa:
            break
    santa_cnt = santa.index(obj)
    return cnt + santa_cnt


def test():
    test_data = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""

    objects = preprocess(test_data)
    assert count_orbits(objects) == 42
    assert get_transfers(objects, 'K') == ['J', 'E', 'D', 'C', 'B', 'COM']



if __name__ == '__main__':
    test()
    fname = './advent2019/day06/input.txt'
    result = part1(fname)
    print(f'Part 1: {result}') # 204521
    result = part1a(fname)
    print(f'Part 1a: {result}') # 204521
    result = part2(fname)
    print(f'Part 2: {result}') # 307
