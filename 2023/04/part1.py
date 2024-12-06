#!/usr/bin/env python
#
# Solution for Advent of Code 2023
# Day 4, part 1
#
# Challenge URL: https://adventofcode.com/2023/day/4
#
# Author: Markus Lindström <markus@markpage.be>
#

import re

SPACE_RE = re.compile(r" {2,}")
CARD_RE = re.compile(r"^Card ([0-9]+): ([^|]+) \| (.*)$")

score = 0
with open("input") as fp:
    for line in fp:
        card_score = 0
        line = SPACE_RE.sub(" ", line.strip())
        match = CARD_RE.match(line)
        card_id = int(match.group(1))
        winning = {int(x) for x in match.group(2).split()}
        having = {int(x) for x in match.group(3).split()}
        for h in having:
            if h in winning:
                if card_score == 0:
                    card_score = 1
                else:
                    card_score *= 2
        score += card_score
        print("Card", card_id, "gives", card_score)

print(score)
