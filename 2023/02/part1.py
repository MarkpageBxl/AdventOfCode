#!/usr/bin/env python
#
# Solution for Advent of Code 2023
# Day 2, part 1
#
# Challenge URL: https://adventofcode.com/2023/day/2
#
# Author: Markus Lindström <markus@markpage.be>
#

import re

GAME_RE = re.compile(r"^Game ([0-9]+): (.*)")

CUBES = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

result = 0
with open("input") as fp:
    for line in fp:
        match = GAME_RE.match(line.strip())
        id = int(match.group(1))
        valid = True
        plays = match.group(2).split("; ")
        for play in plays:
            hand = play.split(", ")
            for i in hand:
                amount, color = i.split()
                amount = int(amount)
                if amount > CUBES[color]:
                    valid = False
                    break
            if not valid:
                break
        if valid:
            result += id
print(result)
