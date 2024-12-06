#!/usr/bin/env python
#
# Solution for Advent of Code 2023
# Day 2, part 2
#
# Challenge URL: https://adventofcode.com/2023/day/2#part2
#
# Author: Markus Lindström <markus@markpage.be>
#

import re
from collections import defaultdict
from functools import reduce

GAME_RE = re.compile(r"^Game ([0-9]+): (.*)")


result = 0
with open("input") as fp:
    for line in fp:
        needed_cubes = defaultdict(int)
        match = GAME_RE.match(line.strip())
        id = int(match.group(1))
        plays = match.group(2).split("; ")
        for play in plays:
            hand = play.split(", ")
            for i in hand:
                amount, color = i.split()
                amount = int(amount)
                needed_cubes[color] = max(amount, needed_cubes[color])
        power = reduce(lambda x, y: x * y, needed_cubes.values(), 1)
        result += power
print(result)
