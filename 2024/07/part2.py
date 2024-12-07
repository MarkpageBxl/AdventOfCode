#!/usr/bin/env python
#
# Solution for Advent of Code 2024
# Day 7, part 2
#
# Challenge URL: https://adventofcode.com/2024/day/7#part2
#
# Author: Markus Lindström <markus@markpage.be>
#

from collections.abc import Iterable


def to_base(n: int, b: int) -> str:
    result = []
    if n == 0:
        return "0"
    while n > 0:
        digit = n % b
        result.insert(0, digit)
        n //= b
    return "".join([str(x) for x in result])


def generate_operators(length: int) -> Iterable[str]:
    length -= 1
    for k in range(3**length):
        ops = to_base(k, 3)
        ops = ops.zfill(length)
        ops = ops.replace("0", "+").replace("1", "*").replace("2", "|")
        yield ops


def main():
    data = []
    with open("input") as fp:
        for line in fp:
            equation = line.strip()
            lhs, rhs = equation.split(":")
            rhs = rhs.strip()
            result, components = int(lhs), tuple([int(x) for x in rhs.split()])
            data.append((result, components))

    total_calibration_result = 0
    for line_no, (result, components) in enumerate(data):
        for operators in generate_operators(len(components)):
            current = components[0]
            for i, operator in enumerate(operators):
                if operator == "+":
                    current += components[i + 1]
                elif operator == "*":
                    current *= components[i + 1]
                else:
                    # concatenation
                    concat = str(current) + str(components[i + 1])
                    current = int(concat)
            if current == result:
                print("MATCH:", result, components, operators)
                total_calibration_result += result
                break

    print(total_calibration_result)


if __name__ == "__main__":
    main()
