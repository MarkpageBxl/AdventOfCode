#!/usr/bin/env python
#
# Solution for Advent of Code 2024
# Day 3, part 1
#
# Challenge URL: https://adventofcode.com/2024/day/3
#
# Author: Markus Lindström <markus@markpage.be>
#

import re

MUL_RE = re.compile(r"mul\(([0-9]+),([0-9]+)\)")

result = 0
with open("input") as fp:
    for line in fp:
        matches = MUL_RE.findall(line)
        for a, b in matches:
            result += int(a) * int(b)

print(result)
