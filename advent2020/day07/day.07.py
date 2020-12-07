'''https://adventofcode.com/2020/day/7'''

from collections import namedtuple


Bag = namedtuple('Bag', 'color qty')


def parse(line):
    line = line.strip('.\n').replace('bags', 'bag').replace(',', '')
    outer, inner = line.split(' contain ')
    outer = outer[:-4]
    inner = inner.split('bag')
    bags = [parse_bag(bag) for bag in inner if bag and bag != 'no other ']
    return (outer, bags)
          

def parse_bag(bag):
    qty, *color = bag.strip().split(' ')
    return Bag(' '.join(color), int(qty))


def rules2colors(rules):
    return {key:[bag.color for bag in value] 
            for key, value in rules.items()}


def get_data(fname):
    rules = {}
    with open(fname) as f:
        for line in f:
            key, value = parse(line)
            rules[key] = value
    return rules


def outer_colors(colors, start):
    all_colors = []
    for key, value in colors.items():
        if start in value:
            all_colors.append(key)
            all_colors.extend(outer_colors(colors, key))
    return set(all_colors)


def inner_bags(colors, start):
    all_bags = 0
    for bag in colors[start]:
        all_bags += bag.qty
        all_bags += inner_bags(colors, bag.color) * bag.qty
    return all_bags


def test():
    test_data = rules2colors(get_data('./advent2020/day07/test_input.txt'))
    assert len(outer_colors(test_data, 'shiny gold')) == 4

def test_part2():
    test_data = get_data('./advent2020/day07/test_input2.txt')
    assert inner_bags(test_data, 'shiny gold') == 126

if __name__ == '__main__':
    test()
    test_part2()
    fname = './advent2020/day07/input.txt'
    rules = get_data(fname)
    print(f"Part 1: {len(outer_colors(rules2colors(rules), 'shiny gold'))}")
    print(f"Part 2: {inner_bags(rules, 'shiny gold')}")
