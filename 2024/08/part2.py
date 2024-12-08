#!/usr/bin/env python
#
# Solution for Advent of Code 2024
# Day 8, part 2
#
# Challenge URL: https://adventofcode.com/2024/day/8#part2
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
            # scan left
            steps = 0
            while True:
                a = (p1[0] - steps * dx, p1[1] - steps * dy)
                if 0 <= a[0] < rows and 0 <= a[1] < cols:
                    antinode_positions.add(a)
                else:
                    break
                steps += 1
            # scan right
            steps = 0
            while True:
                a = (p2[0] + steps * dx, p2[1] + steps * dy)
                if 0 <= a[0] < rows and 0 <= a[1] < cols:
                    antinode_positions.add(a)
                else:
                    break
                steps += 1
    print(len(antinode_positions))


if __name__ == "__main__":
    main()
