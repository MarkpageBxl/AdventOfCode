#!/usr/bin/env python
#
# Solution for Advent of Code 2023
# Day 10, part 2
#
# Challenge URL: https://adventofcode.com/2023/day/10#part2
#
# Author: Markus Lindström <markus@markpage.be>
#

import itertools

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

BOX_CHARS: dict[str, str] = {
    "|": "║",
    "-": "═",
    "L": "╚",
    "J": "╝",
    "7": "╗",
    "F": "╔",
    "S": "╬",
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

    n = len(map)
    m = len(map[0])

    # replace starting position with bend
    accessible_from_start = compute_next_positions(map, start_position)
    accessible_from_start = {
        (x - start_position[0], y - start_position[1]) for x, y in accessible_from_start
    }
    if accessible_from_start.intersection({(1, 0), (0, 1)}):
        # SE
        bend = "F"
    elif accessible_from_start.intersection({(1, 0), (0, -1)}):
        # SW
        bend = "7"
    elif accessible_from_start.intersection({(-1, 0), (0, 1)}):
        # NE
        bend = "L"
    else:
        # NW
        bend = "J"

    map[start_position[0]][start_position[1]] = bend

    # line-by-line scan for inner points

    # Figuring out that flipping inner state depending
    # on edge up/down took me days to figure out!
    # Talk about catharsis at time of writing!
    inner_points = []
    for i in range(n):
        j = 0
        inner = False
        on_edge = None
        while j < m:
            if (i, j) in visited:
                if map[i][j] == "|":
                    inner = not inner
                elif map[i][j] == "-":
                    pass
                elif map[i][j] in "LJ":
                    if not on_edge:
                        on_edge = "up"
                    else:
                        if on_edge == "down":
                            inner = not inner
                        on_edge = None
                elif map[i][j] in "F7":
                    if not on_edge:
                        on_edge = "down"
                    else:
                        if on_edge == "up":
                            inner = not inner
                        on_edge = None
            elif inner:
                inner_points.append((i, j))
            j += 1
    print(len(inner_points))


if __name__ == "__main__":
    main()
