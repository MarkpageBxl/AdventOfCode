#!/usr/bin/env python
#
# Solution for Advent of Code 2024
# Day 8, part 1
#
# Challenge URL: https://adventofcode.com/2024/day/8
#
# Author: Markus Lindström <markus@markpage.be>
#

from collections import defaultdict
import itertools


def main():
    map = []
    with open("input") as fp:
        for line in fp:
            row = list(line.strip())
            map.append(row)
    rows = len(map)
    cols = len(map[0])
    antennae_positions = defaultdict(list)
    for i, row in enumerate(map):
        for j, cell in enumerate(row):
            if cell != ".":
                antennae_positions[cell].append((i, j))
    antinode_positions = set()
    for frequency, positions in antennae_positions.items():
        for p1, p2 in itertools.combinations(positions, r=2):
            dx, dy = p2[0] - p1[0], p2[1] - p1[1]
            a1 = (p1[0] - dx, p1[1] - dy)
            a2 = (p2[0] + dx, p2[1] + dy)
            for x, y in (a1, a2):
                if 0 <= x < rows and 0 <= y < cols:
                    antinode_positions.add((x, y))
    print(len(antinode_positions))


if __name__ == "__main__":
    main()
