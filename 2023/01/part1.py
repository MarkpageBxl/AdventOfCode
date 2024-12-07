#!/usr/bin/env python
#
# Solution for Advent of Code 2023
# Day 1, part 1
#
# Challenge URL: https://adventofcode.com/2023/day/1
#
# Author: Markus Lindström <markus@markpage.be>
#

total = 0
with open("input") as fp:
    for line in fp:
        digits = [x for x in line if x.isdigit()]
        print(digits)
        value = int(digits[0] + digits[-1])
        total += value

print(total)