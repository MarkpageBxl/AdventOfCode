#!/usr/bin/env python
#
# Solution for Advent of Code 2024
# Day 10, part 2
#
# Challenge URL: https://adventofcode.com/2024/day/10#part2
#
# Author: Markus Lindström <markus@markpage.be>
#

from copy import deepcopy
from pprint import pprint
import os

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


def safe_to_int(x: str) -> str | int:
    if x.isdigit():
        return int(x)
    return x


def main():
    map = []
    trailheads = set()
    with open("input") as fp:
        for i, line in enumerate(fp):
            row = [safe_to_int(x) for x in line.strip()]
            map.append(row)
            for j, height in enumerate(row):
                if height == 0:
                    trailheads.add((i, j))
    ratings = {trailhead: 0 for trailhead in trailheads}
    states = {trailhead: {trailhead} for trailhead in trailheads}
    visited = {trailhead: set() for trailhead in trailheads}

    for trailhead in trailheads:
        rating = 0
        previous_state = None
        state = states[trailhead]
        graph = dict()
        # halt when we reach a fixed point
        while state != previous_state:
            previous_state = deepcopy(state)
            state = set()
            for position in previous_state:
                next_positions = compute_next_positions(map, position)
                next_positions.difference_update(visited)
                graph[position] = set(next_positions)
                state.update(next_positions)
                visited[trailhead].add(position)
            if not state:
                break
        # DAG reconstructed, let's walk
        # dump_dot(graph, map)
        stack = [trailhead]
        print(stack)
        while stack:
            pos = stack.pop()
            if len(graph[pos]) == 0 and map[pos[0]][pos[1]] == 9:
                print("rating++")
                rating += 1
            stack.extend(graph[pos])
            print(stack)
        print(rating)
        ratings[trailhead] = rating
    print(ratings)
    print(sum(ratings.values()))


def dump_dot(graph: dict[tuple[int, int], set[tuple[int, int]]], map):
    with open("graph.dot", "w") as fp:
        fp.write("digraph G {\n")
        # fp.write("rankdir=LR;\n")
        for src, dsts in graph.items():
            src_label = f"({src[0]},{src[1]}):{map[src[0]][src[1]]}"
            for dst in dsts:
                dst_label = f"({dst[0]},{dst[1]}):{map[dst[0]][dst[1]]}"
                fp.write(f'"{src_label}" -> "{dst_label}";\n')
        fp.write("}\n")
    os.system("dot -Tpng graph.dot > graph.png")


if __name__ == "__main__":
    main()
