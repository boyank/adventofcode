'''https://adventofcode.com/2019/day/7'''

import logging
import itertools
from collections import namedtuple, deque


Instruction = namedtuple('Instruction', ['opcode', 'param1', 'param2', 'target', 'pos'])
Opcode = namedtuple('Opcode', ['mode3', 'mode2', 'mode1', 'code'])

class Intercode:
    def __init__(self, instructions=None, pos=0, phase=None, input_signal=None, name=None, mode=None):
        self.instructions = [int(num) for num in instructions.split(',')]
        self.pos = pos
        self.phase = phase
        self.input_signal = input_signal
        self.output = None
        self.name = name
        self.mode = mode
        self._initial_state = tuple(self.instructions)


    @property
    def opcode(self):
        return self._read_opcode(self.pos)

    
    @property
    def next_opcode(self):
        return self._read_opcode(self.pos + self.offset)


    def _read_opcode(self, pos):
        code = f'{str(self.instructions[pos]):0>5s}'
        mode3, mode2, mode1 = code[:3]
        return Opcode(int(mode3), int(mode2), int(mode1), int(code[-2:]))


    @property
    def offset(self):
        offsets = {1:4, 2:4, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4}
        return offsets[self.opcode.code]


    @property
    def instruction(self):
        param1 = param2 = param3 = None
        if self.opcode.code in (1, 2, 7, 8):
            param1, param2, param3 = self.instructions[self.pos+1:self.pos + self.offset]
            param1 = param1 if self.opcode.mode1 else self.instructions[param1]
            param2 = param2 if self.opcode.mode2 else self.instructions[param2]
        elif self.opcode.code == 3:
            param3 = self.instructions[self.pos + 1]
        elif self.opcode.code == 4:
            param1 = self.instructions[self.pos + 1]
            param1 = param1 if self.opcode.mode1 else self.instructions[param1]
        elif self.opcode.code in (5, 6):
            param1, param2 = self.instructions[self.pos+1:self.pos + 3]
            param1 = param1 if self.opcode.mode1 else self.instructions[param1]
            param2 = param2 if self.opcode.mode2 else self.instructions[param2]
        return Instruction(self.opcode, param1, param2, param3, self.pos)


    def run(self, reset=True):
        operations = {1:self._add, 2:self._mul, 3:self._input, 4:self._output,
                      5:self._jump_true, 6:self._jump_false, 7:self._lt, 8:self._eq}

        while True:
            opcode = self.opcode.code
            if opcode == 99:
                if reset:
                    self.reset()
                break
            else:
                operations[opcode]()
                if opcode == 4 and self.mode == 'feedback':
                    break

    def _add(self):
        instruction = self.instruction
        result = instruction.param1 + instruction.param2
        self.instructions[instruction.target] = result
        self.pos += self.offset


    def _mul(self):
        instruction = self.instruction
        result = instruction.param1 * instruction.param2
        self.instructions[instruction.target] = result
        self.pos += self.offset


    def _input(self):
        instruction = self.instruction
        if self.phase is not None:
            user_input = self.phase
            self.phase = None
        elif self.input_signal is not None:
            user_input = self.input_signal
            self.input_signal = None
        else:
            user_input = int(input('>>> '))
        self.instructions[instruction.target] = user_input
        self.pos += self.offset


    def _output(self):
        instruction = self.instruction
        self.output = instruction.param1
        if self.next_opcode.code == 99:
            logging.debug(f'DIAGNOSTIC MESSAGE: {instruction.param1}')
        elif self.instruction.param1 != 0:
            logging.debug(f'OUTPUT: {instruction.param1}')
        self.pos += self.offset


    def _jump_true(self):
        instruction = self.instruction
        if instruction.param1:
            self.pos = instruction.param2
        else:
            self.pos += self.offset


    def _jump_false(self):
        instruction = self.instruction
        if not instruction.param1:
            self.pos = instruction.param2
        else:
            self.pos += self.offset


    def _lt(self):
        instruction = self.instruction
        self.instructions[instruction.target] = int(instruction.param1 < instruction.param2)
        self.pos += self.offset


    def _eq(self):
        instruction = self.instruction
        self.instructions[instruction.target] = int(instruction.param1 == instruction.param2)
        self.pos += self.offset


    def reset(self):
        self.instructions = list(self._initial_state)
        self.pos = 0

    def __repr__(self):
        return f'{self.name}: phase:{self.phase}, signal:{self.input_signal}, output:{self.output}'


def part1(data):
    results = []
    for phases in itertools.permutations(range(5)):
        signal = 0
        for phase in phases:
                intercode = Intercode(data, phase=phase, input_signal=signal)
                intercode.run()
                signal = intercode.output
        results.append(signal)
    return results


def part2(data):
    results = []
    for phases in itertools.permutations(range(5, 10)):
        signal = 0
        amplifiers = deque(Intercode(data[::], phase=phase, name=name, mode='feedback') 
                            for phase, name in zip(phases, 'ABCDE'))
        while True:
            amplifier = amplifiers[0]
            amplifier.input_signal = signal
            amplifier.run(reset=False)
            signal = amplifier.output
            if amplifier.opcode.code == 99 and amplifier.name == 'E':
                results.append(signal)
                break
            amplifiers.rotate(-1)
    return results


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    fname = './advent2019/day07/input.txt'
    with open(fname) as f:
        data = f.read()
    

    results = part1(data)
    print(f'part 1. {max(results)}') # 17440


    results = part2(data)
    print(f'part 2. {max(results)}') # 27561242
