#!/usr/bin/env python
#
# Solution for Advent of Code 2023
# Day 10, part 1
#
# Challenge URL: https://adventofcode.com/2023/day/10
#
# Author: Markus Lindström <markus@markpage.be>
#

DIRECTION_TRANSLATIONS: dict[str, tuple[int, int]] = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
}

VALID_DIRECTIONS_FROM_PIPE: dict[str, set[str]] = {
    "L": {"N", "E"},
    "|": {"N", "S"},
    "J": {"N", "W"},
    "F": {"E", "S"},
    "-": {"E", "W"},
    "7": {"S", "W"},
    "S": {"N", "E", "W", "S"},
    ".": set(),
}

DIRECTION_TO_VALID_PIPE: dict[str, set[str]] = {
    "N": {"F", "7", "|"},
    "E": {"7", "-", "J"},
    "W": {"L", "-", "F"},
    "S": {"L", "|", "J"},
}


def compute_next_positions(map: list[list[str]], position: tuple[int, int]):
    current_pipe = map[position[0]][position[1]]
    next_positions = set()
    for direction in VALID_DIRECTIONS_FROM_PIPE[current_pipe]:
        dr, dc = DIRECTION_TRANSLATIONS[direction]
        i, j = position[0] + dr, position[1] + dc
        if (
            0 <= i < len(map)
            and 0 <= j < len(map[0])
            and map[i][j] in DIRECTION_TO_VALID_PIPE[direction]
        ):
            next_positions.add((i, j))
    return next_positions


def main():
    map = []
    start_position = None
    with open("input") as fp:
        for i, line in enumerate(fp):
            row = list(line.strip())
            map.append(row)
            try:
                j = row.index("S")
                start_position = (i, j)
            except ValueError:
                pass
    distance = 0
    state = {start_position}
    visited = set()
    previous_state = set()
    # halt when we reach a fixed point
    while state != previous_state:
        previous_state = state
        state = set()
        for position in previous_state:
            next_positions = compute_next_positions(map, position)
            next_positions.difference_update(visited)
            state.update(next_positions)
            visited.add(position)
        if not state:
            break
        distance += 1
    print(distance)


if __name__ == "__main__":
    main()
