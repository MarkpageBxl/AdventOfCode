#!/usr/bin/env python
#
# Solution for Advent of Code 2023
# Day 3, part 2
#
# Challenge URL: https://adventofcode.com/2023/day/3#part2
#
# Author: Markus Lindström <markus@markpage.be>
#

m: dict[tuple[int, int], str] = dict()

with open("input") as fp:
    dim = 0
    for row, line in enumerate(fp):
        dim += 1
        for col, c in enumerate(line.strip()):
            m[(row, col)] = c


def is_valid_coord(m: dict[tuple[int, int], str], row: int, col: int) -> bool:
    return (row, col) in m


def reconstruct_numbers(
    m: dict[tuple[int, int], str], locations: list[tuple[int, int]]
) -> list[int]:
    result = []
    handled_locations: set[tuple[int, int]] = set()
    for location in locations:
        if location in handled_locations:
            continue
        row, col = location
        digits = [m[location]]
        # scan backward
        k = 1
        while is_valid_coord(m, row, col - k) and m[(row, col - k)].isdigit():
            digits.insert(0, m[(row, col - k)])
            handled_locations.add((row, col - k))
            k += 1
        # scan forward
        k = 1
        while is_valid_coord(m, row, col + k) and m[(row, col + k)].isdigit():
            digits.append(m[(row, col + k)])
            handled_locations.add((row, col + k))
            k += 1
        number = int("".join(digits))
        result.append(number)
    return result


def probe(m: dict[tuple[int, int], str], row: int, col: int) -> list[int]:
    locations = []
    start_row = row - 1
    end_row = row + 1
    start_col = col - 1
    end_col = col + 1
    for r in range(start_row, end_row + 1):
        for c in range(start_col, end_col + 1):
            if is_valid_coord(m, r, c):
                if m[(r, c)].isdigit():
                    # note coordinates around gear candidate
                    # where we have seen a digit
                    locations.append((r, c))
    return reconstruct_numbers(m, locations)


gear_candidates = [k for k in m if m[k] == "*"]
print(gear_candidates)

result = 0
for gear_candidate in gear_candidates:
    numbers = probe(m, *gear_candidate)
    if len(numbers) == 2:
        result += numbers[0] * numbers[1]

print(result)
