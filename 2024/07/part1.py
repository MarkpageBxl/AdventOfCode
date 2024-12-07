#!/usr/bin/env python
#
# Solution for Advent of Code 2024
# Day 7, part 1
#
# Challenge URL: https://adventofcode.com/2024/day/7
#
# Author: Markus Lindström <markus@markpage.be>
#

from collections.abc import Iterable


def generate_operators(length: int) -> Iterable[str]:
    length -= 1
    for k in range(2**length):
        ops = ("{k:0" + str(length) + "b}").format(k=k)
        ops = ops.replace("0", "+").replace("1", "*")
        yield ops


data = []
with open("input") as fp:
    for line in fp:
        equation = line.strip()
        lhs, rhs = equation.split(":")
        rhs = rhs.strip()
        result, components = int(lhs), tuple([int(x) for x in rhs.split()])
        data.append((result, components))

total_calibration_result = 0
for result, components in data:
    for operators in generate_operators(len(components)):
        current = components[0]
        for i, operator in enumerate(operators):
            if operator == "+":
                current += components[i + 1]
            else:
                current *= components[i + 1]
        if current == result:
            print("MATCH:", result, components, operators)
            total_calibration_result += result
            break

print(total_calibration_result)
