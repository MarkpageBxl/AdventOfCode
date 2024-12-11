#!/usr/bin/env python
#
# Solution for Advent of Code 2024
# Day 11, part 1
#
# Challenge URL: https://adventofcode.com/2024/day/11
#
# Author: Markus Lindström <markus@markpage.be>
#

from typing import TextIO
from collections.abc import Iterable, Sequence


def load(fp: TextIO) -> Sequence[int]:
    return [int(x) for x in fp.read().strip().split()]


def blink(state: Sequence[int]) -> Iterable[Sequence[int]]:
    while True:
        next_state = []
        for k in state:
            s = str(k)
            if k == 0:
                next_state.append(1)
            elif len(s) % 2 == 0:
                n = len(s) // 2
                lhs, rhs = int(s[:n]), int(s[n:])
                next_state += [lhs, rhs]
            else:
                next_state.append(k * 2024)
        state = next_state
        yield state


def main():
    with open("input") as fp:
        stones = load(fp)
    generator = blink(stones)
    for i in range(25):
        stones = next(generator)
    print(len(stones))


if __name__ == "__main__":
    main()
