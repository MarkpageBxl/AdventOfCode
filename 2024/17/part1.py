#!/usr/bin/env python
#
# Solution for Advent of Code 2024
# Day 17, part 1
#
# Challenge URL: https://adventofcode.com/2024/day/17
#
# Author: Markus Lindström <markus@markpage.be>
#

# 3 bit computer: programs are a sequence of 3 bit words
# 3 registers (unlimited storage): A, B, C
# + IP (instruction pointer), halts if IP is outside program memory
# IP <- IP + 2 each cycle, except jumps
# 8 opcodes, single operand
# two adressing modes: literal, combo

import re
from typing import TextIO

REGISTER_RE = re.compile(r"^Register ([A-C]): (-?[0-9]+)$")
PROGRAM_RE = re.compile(r"Program: (.*)$")


def load_registers(fp: TextIO) -> tuple[int, int, int]:
    # Load registers
    m = REGISTER_RE.match(next(fp))
    assert m.group(1) == "A"
    a = int(m.group(2))
    m = REGISTER_RE.match(next(fp))
    assert m.group(1) == "B"
    b = int(m.group(2))
    m = REGISTER_RE.match(next(fp))
    assert m.group(1) == "C"
    c = int(m.group(2))
    return a, b, c


def load_program(fp: TextIO) -> list[tuple[int, int]]:
    while not (m := PROGRAM_RE.match(next(fp))):
        pass
    words = m.group(1).split(",")
    instructions = []
    for i in range(0, len(words) - 1, 2):
        instructions.append((int(words[i]), int(words[i + 1])))
    return instructions


# Combo operands:
# 0-3: literal integers
# 4: value of A
# 5: value of B
# 6: value of C
# 7: reserved, invalid
def combo(code: int, registers: tuple[int, int, int]) -> int:
    a, b, c = registers
    if 0 <= code <= 3:
        return code
    if code == 4:
        return a
    if code == 5:
        return b
    if code == 6:
        return c
    assert False


# Opcode table
# 0: adv: A <- A >> (combo operand)
# 1: bxl: B <- B xor (literal operand)
# 2: bst: B <- (combo operand) & 0b111
# 3: jnz: jump to literal operand if A != 0
# 4: bxc: B <- B xor C, ignores operand
# 5: out: output (combo & 0b111) comma separated
# 6: bdv: B <- A >> (combo operand)
# 7: cdv: C <- A >> (combo operand)
def execute(
    program: list[tuple[int, int]], registers: tuple[int, int, int]
) -> tuple[int, tuple[int, int, int]]:
    ip = 0
    a, b, c = registers
    output_buffer = []
    while 0 <= ip < len(program):
        opcode, operand = program[ip]
        if opcode == 0:  # adv
            a = a >> combo(operand, (a, b, c))
        elif opcode == 1:  # bxl
            b = b ^ operand
        elif opcode == 2:  # bst
            b = combo(operand, (a, b, c)) & 0b111
        elif opcode == 3:  # jnz
            if a != 0:
                ip = operand - 1
                # assert alignment
                assert operand % 2 == 0
        elif opcode == 4:  # bxc
            b = b ^ c
        elif opcode == 5:  # out
            output_buffer.append(combo(operand, (a, b, c)) & 0b111)
        elif opcode == 6:  # bdv
            b = a >> combo(operand, (a, b, c))
        elif opcode == 7:  # cdv
            c = a >> combo(operand, (a, b, c))
        else:
            assert False
        ip += 1
    registers = (a, b, c)
    print(",".join([str(x) for x in output_buffer]))
    return ip, registers


def main():
    with open("input") as fp:
        registers = load_registers(fp)
        program = load_program(fp)
    execute(program, registers)


if __name__ == "__main__":
    main()
