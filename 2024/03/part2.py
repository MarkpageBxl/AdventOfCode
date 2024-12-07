#!/usr/bin/env python
#
# Solution for Advent of Code 2024
# Day 3, part 2
#
# Challenge URL: https://adventofcode.com/2024/day/3#part2
#
# Author: Markus Lindström <markus@markpage.be>
#

import re

MUL_RE = re.compile(r"mul\(([0-9]+),([0-9]+)\)|(do)\(\)|(don't)\(\)")

result = 0
enabled = True
with open("input") as fp:
    for line in fp:
        matches = MUL_RE.findall(line)
        for i1, i2, do, dont in matches:
            if enabled and i1 and i2:
                result += int(i1) * int(i2)
            elif do:
                enabled = True
            elif dont:
                enabled = False

print(result)
