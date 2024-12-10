#!/usr/bin/env python
#
# Solution for Advent of Code 2024
# Day 10, part 1
#
# Challenge URL: https://adventofcode.com/2024/day/10
#
# Author: Markus Lindström <markus@markpage.be>
#

from copy import deepcopy

DIRECTION_TRANSLATIONS: dict[str, tuple[int, int]] = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
}


def compute_next_positions(
    map: list[list[str]], position: tuple[int, int]
) -> set[tuple[int, int]]:
    current_height = map[position[0]][position[1]]
    next_positions = set()
    for di, dj in DIRECTION_TRANSLATIONS.values():
        i, j = position[0] + di, position[1] + dj
        if (
            0 <= i < len(map)
            and 0 <= j < len(map[0])
            and map[i][j] == current_height + 1
        ):
            next_positions.add((i, j))
    return next_positions


def main():
    map = []
    trailheads = set()
    with open("input") as fp:
        for i, line in enumerate(fp):
            row = [int(x) for x in line.strip()]
            map.append(row)
            for j, height in enumerate(row):
                if height == 0:
                    trailheads.add((i, j))
    scores = {trailhead: 0 for trailhead in trailheads}
    states = {trailhead: {trailhead} for trailhead in trailheads}
    visited = {trailhead: set() for trailhead in trailheads}
    # halt when we reach a fixed point
    for trailhead in trailheads:
        previous_state = None
        state = states[trailhead]
        score = 0
        while state != previous_state:
            previous_state = deepcopy(state)
            state = set()
            for position in previous_state:
                next_positions = compute_next_positions(map, position)
                next_positions.difference_update(visited)
                state.update(next_positions)
                visited[trailhead].add(position)
            if not state:
                break
        for i, j in visited[trailhead]:
            if map[i][j] == 9:
                score += 1
        scores[trailhead] = score
    print(scores)
    print(sum(scores.values()))


if __name__ == "__main__":
    main()
