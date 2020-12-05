'''https://adventofcode.com/2019/day/1'''

def calc_fuel(mass):
    return int(mass) // 3 - 2


def calc_total_fuel(fuel):
    additional_fuel = calc_fuel(fuel)
    if additional_fuel < 0:
        return fuel
    else:
        return fuel + calc_total_fuel(additional_fuel)


def test():
    test_data = [(12, 2), (14, 2), (1969, 654), (100756, 33583)]
    for mass, fuel in test_data:
        assert fuel == calc_fuel(mass)


def part1():
    with open('./advent2019/day01/input.txt') as f:
        return sum(calc_fuel(mass) for mass in f)


def part2():
    total_fuel = 0
    with open('./advent2019/day01/input.txt') as f:
        for mass in f:
            fuel = calc_fuel(mass)
            total_fuel += fuel
            while True:
                additional_fuel = calc_fuel(fuel)
                if additional_fuel < 0:
                    break
                else:
                    total_fuel += additional_fuel
                    fuel = additional_fuel
    return total_fuel


def part2a():
    total_fuel = 0
    with open('./advent2019/day01/input.txt') as f:
        for mass in f:
            fuel = calc_fuel(mass)
            total_fuel += calc_total_fuel(fuel)
    return total_fuel


if __name__ == '__main__':
    test()
    fuel = part1()
    print(f'Part 1: {fuel}') # 3427972
    total_fuel = part2()
    print(f'Part 2: {total_fuel}') # 5139078

    # alternative part2 - using recursive function
    total_fuel2 = part2a()
    print(f'Part 2: {total_fuel2}') # 5139078