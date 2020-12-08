'''https://adventofcode.com/2020/day/8'''

import logging
import pytest
from collections import namedtuple

Instruction = namedtuple('Instruction', ['opcode', 'value'])


class Emulator:
    def __init__(self, instructions, value=0, pos=0):
        self.instructions = instructions
        self.value = value
        self.pos = pos
        self._log = []
        

    @property
    def log(self):
        return self._log


    @property
    def instructions(self):
        return self._instructions


    @instructions.setter
    def instructions(self, value):
        if isinstance(value, (list, tuple)):
            self._instructions = value
        elif isinstance(value, str):
            self._instructions = []
            for item in value.splitlines():
                opcode, val = item.split(' ')
                self._instructions.append(Instruction(opcode, int(val)))


    def acc(self, value):
        self.value += value

    def jmp(self, value):
        self.pos += value

    def nop(self, value):
        pass

    def run(self):
        while True:
            if self.pos in self.log:
                return self.value
            instruction = self.instructions[self.pos]
            self.log.append(self.pos)
            cmd = getattr(self, instruction.opcode)
            cmd(instruction.value)
            if instruction.opcode != 'jmp':
                self.pos += 1


def part1(fname):
    with open(fname) as f:
        instructions = f.read()
        emulator = Emulator(instructions=instructions)
        return emulator.run()


@pytest.fixture()
def input_data():
    expected = [Instruction('nop', 0), Instruction('acc', 1), Instruction('jmp', 4), 
                Instruction('acc', 3), Instruction('jmp', -3), Instruction('acc', -99),
                Instruction('acc', 1), Instruction('jmp', -4), Instruction('acc', 6)]
    result = 5
    with open('./advent2020/day08/test_input.txt') as f:
        return f.read(), expected, result


@pytest.mark.usefixtures('input_data')
def test_emulator_init(input_data):
    instr, expected, result = input_data
    emulator = Emulator(instr)
    assert emulator.instructions == expected


@pytest.mark.usefixtures('input_data')
def test_emulator_run(input_data):
    instr, expected, result = input_data
    emulator = Emulator(instr)
    emulator.run()
    assert emulator.value == result

if __name__ == '__main__':
    fname = './advent2020/day08/input.txt'
    result = part1(fname)
    print(f'Accumulator value: {result}') # Accumulator value: 1451
