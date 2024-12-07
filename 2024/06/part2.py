#!/usr/bin/env python
#
# Solution for Advent of Code 2024
# Day 6, part 2
#
# Challenge URL: https://adventofcode.com/2024/day/6#part2
#
# Author: Markus Lindström <markus@markpage.be>
#

import copy

DIRECTIONS = {"^": (-1, 0), "v": (1, 0), ">": (0, 1), "<": (0, -1)}


def next_direction(dir: str) -> str:
    if dir == "^":
        return ">"
    if dir == ">":
        return "v"
    if dir == "v":
        return "<"
    if dir == "<":
        return "^"
    else:
        assert False


def print_map(map):
    for row in map:
        print(" ".join(row))


with open("input") as fp:
    base_map: list[list[str]] = [list(line.strip()) for line in fp]

# locate guard
base_guard_position = None
for i, row in enumerate(base_map):
    try:
        base_guard_position = (i, row.index("^"))
        break
    except:
        pass

# we could narrow down candidates to only places where the guard goes, but meh
candidate_obstructions = [
    (x, y)
    for x in range(len(base_map))
    for y in range(len(base_map))
    if base_map[x][y] not in ("#", "^", "v", "<", ">")
]
valid_obstructions = 0
guard_position = base_guard_position
base_guard_direction = base_map[guard_position[0]][guard_position[1]]
guard_direction = base_guard_position
for candidate_obstruction in candidate_obstructions:
    map = copy.deepcopy(base_map)
    guard_position = base_guard_position
    guard_direction = base_guard_direction

    # put new obstruction
    map[candidate_obstruction[0]][candidate_obstruction[1]] = "O"
    visited_positions: set[tuple[int, int, str]] = set()

    while True:
        if (guard_position[0], guard_position[1], guard_direction) in visited_positions:
            valid_obstructions += 1
            break
        visited_positions.add((guard_position[0], guard_position[1], guard_direction))
        candidate_pos = (
            guard_position[0] + DIRECTIONS[guard_direction][0],
            guard_position[1] + DIRECTIONS[guard_direction][1],
        )
        if (
            candidate_pos[0] == len(map)
            or candidate_pos[0] < 0
            or candidate_pos[1] == len(map)
            or candidate_pos[1] < 0
        ):
            # guard has exited map
            break
        if map[candidate_pos[0]][candidate_pos[1]] in ("#", "O"):
            guard_direction = next_direction(guard_direction)
        else:
            guard_position = candidate_pos
            map[guard_position[0]][guard_position[1]] = guard_direction

print(valid_obstructions)
