#!/usr/bin/env python
#
# Solution for Advent of Code 2024
# Day 11, part 2
#
# Challenge URL: https://adventofcode.com/2024/day/11#part2
#
# Author: Markus Lindström <markus@markpage.be>
#

import cProfile
from collections import defaultdict
from collections.abc import Iterable, Sequence
from typing import TextIO, TypeVar
from copy import copy
from pprint import pprint

T = TypeVar("T")
Multiset = dict[T, int]


def load(fp: TextIO) -> Multiset[int]:
    lst = [int(x) for x in fp.read().strip().split()]
    d = defaultdict(int)
    d.update({x: lst.count(x) for x in lst})
    return d


def update_mset(mset: Multiset[int], remove: int, add: set[int], times: int):
    mset[remove] -= times
    assert mset[remove] >= 0
    if mset[remove] == 0:
        del mset[remove]
    for k in add:
        mset[k] += times


def blink(state: Multiset[int]) -> Iterable[Multiset[int]]:
    state_graph: dict[int, Sequence[int]] = {}
    while True:
        next_state = copy(state)
        for k, v in state.items():
            if k not in state_graph:
                s = str(k)
                if k == 0:
                    next_states = (1,)
                elif len(s) % 2 == 0:
                    next_states = split(s)
                else:
                    next_states = (k * 2024,)
                state_graph[k] = next_states
            update_mset(next_state, k, state_graph[k], times=v)
        state = next_state
        yield state


def split(s: str) -> Sequence[int]:
    n = len(s) // 2
    lhs, rhs = int(s[:n]), int(s[n:])
    return (lhs, rhs)


def main():
    with open("input") as fp:
        stones = load(fp)
    generator = blink(stones)
    for i in range(75):
        print("Round:", i + 1)
        stones = next(generator)
    print("Stones:", sum(stones.values()))


if __name__ == "__main__":
    main()
