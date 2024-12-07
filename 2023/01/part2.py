#!/usr/bin/env python
#
# Solution for Advent of Code 2023
# Day 1, part 2
#
# Challenge URL: https://adventofcode.com/2023/day/1#part2
#
# Author: Markus Lindström <markus@markpage.be>
#

DIGITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five" : 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

total = 0
with open("input") as fp:
    for line in fp:
        i = 0
        while i < len(line):
            start = i
            if line[i].isdigit():
                i += 1
                continue
            digit_found = False
            for key, value in DIGITS.items():
                if line[i:i+len(key)] == key:
                    line = line.replace(key, str(value), 1)
                    i += 1
                    digit_found = True
                    break
            if not digit_found:
                i += 1
        digits = ''.join([x for x in line if x.isdigit()])
        value = int(digits[0] + digits[-1])
        total += value

print(total)