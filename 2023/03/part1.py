#!/usr/bin/env python
#
# Solution for Advent of Code 2023
# Day 3, part 1
#
# Challenge URL: https://adventofcode.com/2023/day/3
#
# Author: Markus Lindström <markus@markpage.be>
#

from typing import Optional

m: dict[tuple[int, int], str] = dict()

with open("input") as fp:
    dim = 0
    for row, line in enumerate(fp):
        dim += 1
        for col, c in enumerate(line.strip()):
            m[(row, col)] = c


def is_valid_coord(m: dict[tuple[int, int], str], row: int, col: int) -> bool:
    return (row, col) in m


def probe(m: dict[tuple[int, int], str], row: int, col: int, length: int) -> bool:
    start_row = row - 1
    end_row = row + 1
    start_col = col - 1
    end_col = col + length
    for r in range(start_row, end_row + 1):
        for c in range(start_col, end_col + 1):
            if is_valid_coord(m, r, c):
                if not m[(r, c)].isdigit() and m[(r, c)] != ".":
                    return True
    return False


result = 0
for row in range(dim):
    col = 0
    buffer = ""
    part_nr: Optional[int] = None
    nr_start: Optional[int] = None
    while col < dim:
        if m[(row, col)].isdigit():
            if nr_start is None:
                nr_start = col
            buffer += m[(row, col)]
        else:
            if buffer:
                part_nr = int(buffer)
                if probe(m, row, nr_start, len(buffer)):
                    print(part_nr, "added")
                    result += part_nr
                else:
                    print(part_nr, "skipped")
                nr_start = None
                buffer = ""
        col += 1

    if buffer:
        part_nr = int(buffer)
        if probe(m, row, nr_start, len(buffer)):
            print(part_nr, "added")
            result += part_nr

print(result)
