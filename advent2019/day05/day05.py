from collections import namedtuple
import logging

Instruction = namedtuple('Instruction', ['opcode', 'param1', 'param2', 'target', 'pos'])
Opcode = namedtuple('Opcode', ['mode3', 'mode2', 'mode1', 'code'])

class Intercode:
    def __init__(self, instructions=None, pos=0):
        self.instructions = [int(num) for num in instructions.split(',')]
        self.pos = pos


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
        offsets = {1:4, 2:4, 3:2, 4:2}
        return offsets[self.opcode.code]


    @property
    def instruction(self):
        param1 = param2 = param3 = None
        if self.opcode.code in (1, 2):
            param1, param2, param3 = self.instructions[self.pos+1:self.pos + self.offset]
            param1 = param1 if self.opcode.mode1 else self.instructions[param1]
            param2 = param2 if self.opcode.mode2 else self.instructions[param2]
        elif self.opcode.code == 3:
            param3 = self.instructions[self.pos + 1]
        elif self.opcode.code == 4:
            param1 = self.instructions[self.pos + 1]
            param1 = param1 if self.opcode.mode1 else self.instructions[param1]
        return Instruction(self.opcode, param1, param2, param3, self.pos)


    def run(self):
        operations = {1:self._add, 2:self._mul, 3:self._input, 4:self._output}
        while True:
            if self.opcode.code == 99:
                print('--- END CODE 99 ---')
                break
            else:
                operations[self.opcode.code]()

    def _add(self):
        instruction = self.instruction
        logging.debug(f'Addition: {instruction}')
        result = instruction.param1 + instruction.param2
        self.instructions[instruction.target] = result
        self.pos += self.offset


    def _mul(self):
        instruction = self.instruction
        logging.debug(f'Multiplication: {instruction}')
        result = instruction.param1 * instruction.param2
        self.instructions[instruction.target] = result
        self.pos += self.offset


    def _input(self):
        instruction = self.instruction
        logging.debug(f'Input: {instruction}')
        user_input = int(input('>>> '))
        self.instructions[instruction.target] = user_input
        self.pos += self.offset


    def _output(self):
        instruction = self.instruction
        logging.debug(f'Output: {instruction}')
        if self.next_opcode.code == 99:
            print(f'DIAGNOSTIC MESSAGE: {instruction.param1}')
        elif self.instruction.param1 != 0:
            logging.critical(f'ERROR MESSAGE: {instruction.param1}')
            raise ValueError(f'ERROR POS: {self.pos}')
        self.pos += self.offset


def part1(fname):
    with open(fname) as f:
        data = f.read()
        intercode = Intercode(data)
        intercode.run()



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    fname = './advent2019/day05/input.txt'
    part1(fname)