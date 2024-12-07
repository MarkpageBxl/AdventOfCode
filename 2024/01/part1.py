#!/usr/bin/env python
#
# Solution for Advent of Code 2024
# Day 1, part 1
#
# Challenge URL: https://adventofcode.com/2024/day/1
#
# Author: Markus Lindström <markus@markpage.be>
#

l1 = []
l2 = []

with open("input") as fp:
    for line in fp:
        left, right = line.strip().split()
        i1, i2 = int(left), int(right)
        l1.append(i1)
        l2.append(i2)

l1.sort()
l2.sort()

total_distance = 0

for a, b in zip(l1, l2):
    distance = abs(b - a)
    total_distance += distance

print(total_distance)
