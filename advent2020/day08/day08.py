'''https://adventofcode.com/2020/day/8'''

import logging
import pytest
from collections import namedtuple

Instruction = namedtuple('Instruction', ['opcode', 'value'])


class Emulator:
    def __init__(self, instructions, seed=0, pos=0):
        self.instructions = instructions
        self.value = self.seed = seed
        self.start = self.pos = pos
        self._log = []
        self.success = None
        

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
        self.pos += 1

    def jmp(self, value):
        self.pos += value

    def nop(self, value):
        self.pos += 1

    def run(self):
        self._log = []
        self.value = self.seed
        self.success = False
        self.pos = self.start
        while True:
            if self.pos in self.log or self.success:
                break
            instruction = self.instructions[self.pos]
            self.log.append(self.pos)
            cmd = getattr(self, instruction.opcode)
            cmd(instruction.value)
            self.success = self.pos > len(self.instructions) - 1
        return self.value

    def run_diagnostic(self):
        orig_state = self.instructions[::]
        test_positions = [idx for idx, instr in enumerate(self.instructions) if instr.opcode != 'acc']
        for pos in test_positions:
            instr = self.instructions[pos]
            new_code = 'jmp' if instr.opcode == 'nop' else 'nop'
            self.instructions[pos] = Instruction(new_code, instr.value)
            result = self.run()
            self.instructions = orig_state[::]
            if self.success:
                return self.success, self.value, pos, instr.opcode, new_code
        return self.success, self.value, None, None, None



def part1(fname):
    with open(fname) as f:
        instructions = f.read()
        emulator = Emulator(instructions=instructions)
        return emulator.run()

def part2(fname):
    with open(fname) as f:
        instructions = f.read()
        emulator = Emulator(instructions=instructions)
        return emulator.run_diagnostic()


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


@pytest.mark.usefixtures('input_data')
def test_emulator_diagnostic(input_data):
    instr, expected, result = input_data
    emulator = Emulator(instr)
    assert emulator.run_diagnostic()  == (True, 8, 7, 'jmp', 'nop')


def test_aoc():
    fname = './advent2020/day08/input.txt'
    result = part1(fname)
    assert result == 1451
    success, result, *_ = part2(fname)
    assert result == 1160


if __name__ == '__main__':
    fname = './advent2020/day08/input.txt'
    result = part1(fname)
    print(f'Accumulator value: {result}') # Accumulator value: 1451
    success, result, *_ = part2(fname)
    print(f'Accumulator value: {result}') # Accumulator value: 1160