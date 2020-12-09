'''https://adventofcode.com/2019/day/8#part2'''

def get_data(fname):
    with open(fname) as f:
        return f.read().strip()

def get_layers(data, width, height):
    pixels = width * height
    return [data[idx:idx + pixels] for idx in range(0, len(data), pixels)]


def part1(data, width, height):
    layer = min(get_layers(data, width, height), key=lambda layer: layer.count('0'))
    return layer.count('1') * layer.count('2')


def part2(data, width, height):
    visible_pixels = []
    for idx in range(width * height):
        for layer in get_layers(data, width, height):
            pixel = layer[idx]
            if pixel in ['0', '1']:
                visible_pixels.append('▓' if pixel == '0' else ' ')
                break
    return '\n'.join(get_layers(''.join(visible_pixels), width, 1))


def test_get_layers():
    data = '123456789012'
    assert get_layers(data, 3, 2) == ['123456', '789012']


def test_visible_image():
    data = '0222112222120000'
    assert part2(data, 2, 2) == '▓ \n ▓'


if __name__ == '__main__':
    fname = './advent2019/day08/input.txt'
    data = get_data(fname)
    print(f'Part1: {part1(data, 25, 6)}')
    print(f'Part2:\n{part2(data, 25, 6)}')

'''
Part1: 2975
Part2:
    ▓ ▓▓ ▓   ▓▓ ▓▓ ▓    ▓
 ▓▓▓▓ ▓▓ ▓ ▓▓ ▓ ▓▓ ▓ ▓▓▓▓
   ▓▓    ▓ ▓▓ ▓ ▓▓ ▓   ▓▓
 ▓▓▓▓ ▓▓ ▓   ▓▓ ▓▓ ▓ ▓▓▓▓
 ▓▓▓▓ ▓▓ ▓ ▓ ▓▓ ▓▓ ▓ ▓▓▓▓
    ▓ ▓▓ ▓ ▓▓ ▓▓  ▓▓    ▓
'''