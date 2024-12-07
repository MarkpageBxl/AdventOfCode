#!/usr/bin/env python
#
# Solution for Advent of Code 2023
# Day 8, part 1
#
# Challenge URL: https://adventofcode.com/2023/day/8
#
# Author: Markus Lindström <markus@markpage.be>
#

from collections.abc import Iterable
import re

NODE_RE = re.compile(r"^([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)$")

START = "AAA"
GOAL = "ZZZ"


def generate_directions(dirs: str) -> Iterable[str]:
    n = len(dirs)
    i = 0
    while True:
        yield dirs[i]
        i += 1
        if i == len(dirs):
            i = 0


def main():
    with open("input") as fp:
        dirs = next(fp).strip()
        direction_iterator = generate_directions(dirs)
        next(fp)
        nodes: dict[str, tuple[str, str]] = {}
        for line in fp:
            match = NODE_RE.match(line.rstrip())
            node, left, right = match.groups()
            nodes[node] = (left, right)

    current_node = START
    steps = 0
    while current_node != GOAL:
        direction = next(direction_iterator)
        index = 0 if direction == "L" else 1
        current_node = nodes[current_node][index]
        steps += 1

    print(steps)


if __name__ == "__main__":
    main()
