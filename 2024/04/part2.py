#!/usr/bin/env python
#
# Solution for Advent of Code 2024
# Day 4, part 2
#
# Challenge URL: https://adventofcode.com/2024/day/4#part2
#
# Author: Markus Lindström <markus@markpage.be>
#

PATTERN = "MAS"

count = 0

with open("input") as fp:
    data = [line.strip() for line in fp]

dimension = len(data)

for i in range(dimension - 2):
    for j in range(dimension - 2):
        diag1 = ""
        diag2 = ""
        for k in range(3):
            diag1 += data[i + k][j + k]
            diag2 += data[i - k + 2][j + k]
        if (
            (diag1 == PATTERN and diag2 == PATTERN)
            or (diag1 == PATTERN and diag2 == PATTERN[::-1])
            or (diag1 == PATTERN[::-1] and diag2 == PATTERN)
            or (diag1 == PATTERN[::-1] and diag2 == PATTERN[::-1])
        ):
            count += 1


print("total:", count)
