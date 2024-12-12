#!/usr/bin/env python
#
# Solution for Advent of Code 2024
# Day 12, part 1
#
# Challenge URL: https://adventofcode.com/2024/day/12
#
# Author: Markus Lindström <markus@markpage.be>
#

from collections import defaultdict, deque

DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))


def grow_region(
    map: list[list[str]],
    region_queue: deque[tuple[int, int]],
    non_region_set: set[tuple[int, int]],
    visited: set[tuple[int, int]],
):
    n = len(map)
    m = len(map[0])
    region = []
    while len(region_queue) > 0:
        i, j = region_queue.popleft()
        if (i, j) in visited:
            continue
        plant = map[i][j]
        for di, dj in DIRECTIONS:
            x, y = i + di, j + dj
            if (x, y) not in visited and 0 <= x < n and 0 <= y < m:
                if map[x][y] == plant:
                    region_queue.append((x, y))
                else:
                    non_region_set.add((x, y))
        region.append((i, j))
        visited.add((i, j))
    non_region_set.difference_update(visited)
    return region


def main():
    with open("input") as fp:
        map = [list(x.strip()) for x in fp]
    n = len(map)
    m = len(map[0])
    regions: list[list[tuple[int, int]]] = []
    visited: set[tuple[int, int]] = set()
    region_queue = deque()
    non_region_set = set()
    non_region_set.add((0, 0))
    while len(non_region_set) > 0:
        region_queue.append(non_region_set.pop())
        region = grow_region(map, region_queue, non_region_set, visited)
        regions.append(region)

    total_cost = 0
    for region in regions:
        area = 0
        perimeter = 0
        region.sort(key=lambda x: (x[0], x[1]))
        region_set = set(region)
        # horizontal sweep
        for i, j in region:
            for di, dj in DIRECTIONS:
                if (i + di, j + dj) not in region_set:
                    perimeter += 1
        area = len(region)
        cost = area * perimeter
        print("A=", area, " P=", perimeter, " C=", cost, sep="")
        total_cost += cost
    print(total_cost)


if __name__ == "__main__":
    main()
