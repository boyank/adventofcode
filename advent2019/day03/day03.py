from operator import add, sub

def grid(wire, start=(0, 0)):
    wire = wire.split(',')
    wiring=[start]
    directions = {'R':add, 'U':add, 'L':sub, 'D':sub}
    for item in wire:
        direction = directions[item[0]]
        steps = int(item[1:])
        x, y = wiring[-1]
        for _ in range(steps):
            if item.startswith(('R', 'L')):
                x = direction(x, 1)
            else:
                y = direction(y, 1)
            wiring.append((x, y))
    return wiring


def shortest_signal(w1, w2):
    signals = []
    wire1 = grid(w1)
    wire2 = grid(w2)
    intersections = set(wire1).intersection(set(wire2)) - {(0, 0)}
    for intersection in intersections:
        idx1 = wire1.index(intersection)
        idx2 = wire2.index(intersection)
        signals.append(idx1 + idx2)
    return min(signals)

def manhatan_distance(point1, point2=(0, 0)):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def test():
    test_data = [('R8,U5,L5,D3', 'U7,R6,D4,L4', 6, 30), 
                ('R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83', 159, 610), 
                 
                 ('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7', 135, 410)]


    for w1, w2, d, d2 in test_data:
        wire1 = set(grid(w1)) - {(0, 0)}
        wire2 = set(grid(w2)) - {(0, 0)}
        assert d == manhatan_distance((sorted(wire1.intersection(wire2), key=manhatan_distance)[0]))
        assert d2 == shortest_signal(w1, w2)


def part1():
    with open('./advent2019/day03/input.txt') as f:
        w1, w2 = f
        wire1 = set(grid(w1)) - {(0, 0)}
        wire2 = set(grid(w2)) - {(0, 0)}
        return sorted(wire1.intersection(wire2), key=manhatan_distance)[0]


def part2():
    with open('./advent2019/day03/input.txt') as f:
        w1, w2 = f
        return shortest_signal(w1, w2)


if __name__ == '__main__':
    test()
    distance = manhatan_distance(part1())
    print(f'Part 1: {distance}') # 1225
    signal = part2()
    print(f'Part 2: {signal}') # 107036