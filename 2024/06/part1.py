#!/usr/bin/env python

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
    map: list[list[str]] = [list(line.strip()) for line in fp]

# locate guard
guard_position = None
for i, row in enumerate(map):
    try:
        guard_position = (i, row.index("^"))
        break
    except:
        pass

print("Guard starts at:", guard_position)

guard_on_map = True
guard_direction = map[guard_position[0]][guard_position[1]]
print(guard_direction)
while guard_on_map:
    candidate_pos = (
        guard_position[0] + DIRECTIONS[guard_direction][0],
        guard_position[1] + DIRECTIONS[guard_direction][1],
    )
    map[guard_position[0]][guard_position[1]] = "X"
    if candidate_pos[0] == len(map) or candidate_pos[1] == len(map):
        guard_on_map = False
        break
    if map[candidate_pos[0]][candidate_pos[1]] == "#":
        guard_direction = next_direction(guard_direction)
    else:
        guard_position = candidate_pos
        map[guard_position[0]][guard_position[1]] = guard_direction

steps = 0
for row in map:
    steps += row.count("X")

print(steps)
