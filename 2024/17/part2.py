#!/usr/bin/env python
#
# Solution for Advent of Code 2024
# Day 17, part 2
#
# Challenge URL: https://adventofcode.com/2024/day/17#part2
#
# Author: Markus Lindström <markus@markpage.be>
#

# 3 bit computer: programs are a sequence of 3 bit words
# 3 registers (unlimited storage): A, B, C
# + IP (instruction pointer), halts if IP is outside program memory
# IP <- IP + 2 each cycle, except jumps
# 8 opcodes, single operand
# two adressing modes: literal, combo

import logging
import re
from typing import Iterable, TextIO

from utils import disassemble, disassemble_instr

REGISTER_RE = re.compile(r"^Register ([A-C]): (-?[0-9]+)$")
PROGRAM_RE = re.compile(r"Program: (.*)$")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("asm")


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


def load_program(fp: TextIO) -> tuple[list[int], list[tuple[int, int]]]:
    while not (m := PROGRAM_RE.match(next(fp))):
        pass
    words = [int(x) for x in m.group(1).split(",")]
    program = batched(words)
    return words, program


def batched(iterable: Iterable[str]) -> Iterable[tuple[int, int]]:
    batches = []
    for i in range(0, len(iterable) - 1, 2):
        batches.append((iterable[i], iterable[i + 1]))
    return batches


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
) -> tuple[int, tuple[int, int, int], list[int]]:
    ip = 0
    a, b, c = registers
    output_buffer = []
    while 0 <= ip < len(program):
        opcode, operand = program[ip]
        dasm = disassemble_instr(opcode, operand)
        logger.debug("INSTR: %s", dasm)
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
                logger.debug("=" * 15)
        elif opcode == 4:  # bxc
            b = b ^ c
        elif opcode == 5:  # out
            out = combo(operand, (a, b, c)) & 0b111
            output_buffer.append(out)
            logger.debug("OUT: %d", out)
        elif opcode == 6:  # bdv
            b = a >> combo(operand, (a, b, c))
        elif opcode == 7:  # cdv
            c = a >> combo(operand, (a, b, c))
        else:
            assert False
        logger.debug("REGS: A=%d B=%d C=%d", a, b, c)
        ip += 1
    registers = (a, b, c)
    return ip, registers, output_buffer


def reverse_flow(a0, k) -> tuple[int, int, int]:
    c = ((a0 << 3) | k) >> (k ^ 1)
    b = (((k ^ 1) ^ c) ^ 6) & 7
    a = (a << 3) | k
    return a, b, c


def main():
    with open("input") as fp:
        registers = load_registers(fp)
        words, program = load_program(fp)

    # use a backtracking algorithm
    found, a = compute_a(a=0, words=list(reversed(words)))
    print(found, a)
    assert found

    _, b, c = registers
    _, _, output_buffer = execute(program, (a, b, c))
    output_program = batched(output_buffer)
    print(a)
    print(output_program == program)


def compute_a(a, words) -> tuple[bool, int]:
    logger.info("a = %d", a)
    logger.info("words = %s", str(words))
    if len(words) == 0:
        return True, a
    for k in range(8):
        c = compute_c(a, k)
        b = compute_b(k, c)
        out_b = b & 7
        if out_b == words[0]:
            next_a = (a << 3) | k
            logging.info("advancing with k = %d", k)
            found, new_a = compute_a(next_a, words[1:])
            if found:
                return True, new_a
            else:
                logger.info("backtracking, continuing from k = %d", k)
    return False, a


def compute_b(k, c):
    return (k ^ 1) ^ c ^ 6


def compute_c(a, k):
    return ((a << 3) | k) >> (k ^ 1)


if __name__ == "__main__":
    main()
