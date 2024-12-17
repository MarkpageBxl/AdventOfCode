#!/usr/bin/env python
#
# Solution for Advent of Code 13
# Day 2024, part 1
#
# Challenge URL: https://adventofcode.com/13/day/2024
#
# Author: Markus Lindström <markus@markpage.be>
#

from dataclasses import dataclass
import re

BUTTON_RE = re.compile(r"^Button [AB]: X\+([0-9]+), Y\+([0-9]+)$")
PRIZE_RE = re.compile(r"^Prize: X=([0-9]+), Y=([0-9]+)$")

A_TOKENS = 3
B_TOKENS = 1
MAX_MOVES = 100

@dataclass
class ClawMachine:
    ax: int
    ay: int
    bx: int
    by: int
    px: int
    py: int

def play(machine: ClawMachine, moves: list = []):
    best_tokens = 0
    best_moveset = None
    moveset = [0,0]
    while True:
        tokens = moveset[0] * A_TOKENS + moveset[1] * B_TOKENS
        x = moveset[0] * machine.ax + moveset[1] * machine.bx
        y = moveset[0] * machine.ay + moveset[1] * machine.by
        if x == machine.px and y == machine.py:
            if best_moveset is None or tokens < best_tokens:
                best_tokens = tokens
                best_moveset = moveset[:]
                continue
        moveset[1] += 1
        if moveset[1] == 101:
            moveset[1] = 0
            moveset[0] += 1
            if moveset[0] == 101:
                break
    return best_moveset, best_tokens


def main():
    machines = []
    with open("input") as fp:
        try:
            while True:
                m = BUTTON_RE.match(next(fp))
                ax, ay = int(m.group(1)), int(m.group(2))
                m = BUTTON_RE.match(next(fp))
                bx, by = int(m.group(1)), int(m.group(2))
                m = PRIZE_RE.match(next(fp))
                px, py = int(m.group(1)), int(m.group(2))
                machine = ClawMachine(ax, ay, bx, by, px, py)
                machines.append(machine)
                next(fp)
        except StopIteration:
            pass
    
    total_tokens = 0
    for i, machine in enumerate(machines):
        moveset, tokens = play(machine)
        if moveset:
            total_tokens += tokens
    print(total_tokens)


if __name__ == "__main__":
    main()
