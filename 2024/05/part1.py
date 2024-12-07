#!/usr/bin/env python
#
# Solution for Advent of Code 2024
# Day 5, part 1
#
# Challenge URL: https://adventofcode.com/2024/day/5
#
# Author: Markus Lindström <markus@markpage.be>
#

from collections import defaultdict

rules = defaultdict(list)
updates: list[list[int]] = []
with open("input") as fp:
    rule_mode = True
    for line in fp:
        if not line.strip():
            rule_mode = False
            continue
        if rule_mode:
            s = [x for x in line.strip().split("|")]
            dependency = int(s[0])
            target = int(s[1])
            rules[target].append(dependency)
        else:
            updates.append([int(x) for x in line.strip().split(",")])

middle_pages = 0

for update in updates:
    valid = True
    for i in range(len(update)-1):
        if update[i] not in rules[update[i+1]]:
            valid = False
            break
    if valid:
        middle_pages += update[len(update) // 2]

print(middle_pages)