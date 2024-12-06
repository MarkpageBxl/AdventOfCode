#!/usr/bin/env python
#
# Solution for Advent of Code 2023
# Day 4, part 2
#
# Challenge URL: https://adventofcode.com/2023/day/4#part2
#
# Author: Markus Lindström <markus@markpage.be>
#

import re
from queue import Queue

SPACE_RE = re.compile(r" {2,}")
CARD_RE = re.compile(r"^Card ([0-9]+): ([^|]+) \| (.*)$")

card_scores: dict[int, int] = {}

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
                card_score += 1
        card_scores[card_id] = card_score

total_cards = 0
card_queue: Queue[int] = Queue()
for card_id in card_scores:
    card_queue.put(card_id)

while not card_queue.empty():
    card_id = card_queue.get()
    total_cards += 1
    card_score = card_scores[card_id]
    for k in range(card_score):
        card_queue.put(card_id + k + 1)

print(total_cards)
