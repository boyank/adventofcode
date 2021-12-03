def get_data(fname):
    with open(fname) as f:
        return [line.split(' ') for line in f.read().splitlines()]

class Submarine:
    def __init__(self, position=0, depth=0, aim=0):
        self.pos = position
        self.depth = depth
        self.aim = aim

    def move(self, cmd, value):
        if cmd == 'forward':
            self.pos += value
        elif cmd == 'down':
            self.depth += value
        elif cmd == 'up':
            self.depth -= value
        else:
            raise ValueError('Unknow command')
    

    def move2(self, cmd, value):
        if cmd == 'forward':
            self.pos += value
            self.depth += self.aim * value
        elif cmd == 'down':
            self.aim += value
        elif cmd == 'up':
            self.aim -= value
        else:
            raise ValueError('Unknow command')

if __name__ == '__main__':
    submarine = Submarine()
    data = get_data('./advent2021/day02/input.txt')
    for cmd, value in data:
        submarine.move(cmd, int(value))
    print(submarine.depth * submarine.pos) # 2091984


    submarine = Submarine()
    for cmd, value in data:
        submarine.move2(cmd, int(value))
    print(submarine.depth * submarine.pos) # 2086261056
    