#!/usr/bin/env python
#
# Solution for Advent of Code 2023
# Day 6, part 2
#
# Challenge URL: https://adventofcode.com/2023/day/6#part2
#
# Author: Markus Lindström <markus@markpage.be>
#

with open("demo2") as fp:
    for line in fp:
        pass


import re

HEADER_RE = re.compile(r"^[A-Za-z]+: +")

with open("input") as fp:
    times = next(fp).strip()
    times = HEADER_RE.sub("", times).split()
    distances = next(fp).strip()
    distances = HEADER_RE.sub("", distances).split()
    race = (int("".join(times)), int("".join(distances)))

print(race)

# time = hold time + move time
# hold time = (time - move time)
# move time = (time - hold time)
# speed = hold time
# distance = move time * speed
# we need: distance > record
#    move time * hold time > record
#    hold time * (time - hold time) > record


time, record = [int(x) for x in race]
ways_to_win = 0
for hold_time in range(1, time):
    distance = hold_time * (time - hold_time)
    if distance > record:
        ways_to_win += 1

print("Answer:", ways_to_win)
