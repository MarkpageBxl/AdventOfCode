#!/usr/bin/env python
#
# Solution for Advent of Code 2023
# Day 8, part 2
#
# Challenge URL: https://adventofcode.com/2023/day/8#part2
#
# Author: Markus Lindström <markus@markpage.be>
#

import math
import re
from collections import defaultdict
from collections.abc import Iterable

NODE_RE = re.compile(r"^([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)$")

START = "AAA"
GOAL = "ZZZ"


def generate_directions(dirs: str) -> Iterable[tuple[int, str]]:
    n = len(dirs)
    i = 0
    while True:
        yield i, dirs[i]
        i += 1
        if i == len(dirs):
            i = 0


def main():
    with open("input") as fp:
        dirs = next(fp).strip()
        next(fp)
        nodes: dict[str, tuple[str, str]] = {}
        for line in fp:
            match = NODE_RE.match(line.rstrip())
            node, left, right = match.groups()
            nodes[node] = (left, right)

    start_nodes = [node for node in nodes if node[2] == "A"]
    z_steps = defaultdict(list)
    for start_node in start_nodes:
        visited_states = set()
        direction_iterator = generate_directions(dirs)
        node = start_node
        counter = 0
        while True:
            if node[2] == "Z":
                # goal node
                z_steps[start_node].append(counter)
            state_index, direction = next(direction_iterator)
            direction_index = 0 if direction == "L" else 1
            if (node, state_index) in visited_states:
                # cycle detected
                break
            visited_states.add((node, state_index))
            node = nodes[node][direction_index]
            counter += 1
    print(z_steps)
    # we now just need to compute the lcm
    steps = 1
    for z in z_steps.values():
        steps = math.lcm(steps, *z)
    print(steps)


if __name__ == "__main__":
    main()
