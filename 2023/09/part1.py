#!/usr/bin/env python
#
# Solution for Advent of Code 2023
# Day 9, part 1
#
# Challenge URL: https://adventofcode.com/2023/day/9
#
# Author: Markus Lindström <markus@markpage.be>
#


def alternate(coeffs: list[int]):
    result = coeffs[:]
    for i in range(1, len(result), 2):
        result[i] *= -1
    return result


def next_coeffs(coeffs: list[int]):
    # compute next level of binomial coefficients
    if not coeffs:
        return [1]
    result = []
    n = len(coeffs) + 1
    for k in range(n):
        # (n, k) = (n - 1, k - 1) + (n - 1, k)
        left = coeffs[k - 1] if k >= 1 else 0
        right = coeffs[k] if k < n - 1 else 0
        result.append(left + right)
    return result


def main():
    with open("input") as fp:
        reports: list[list[int]] = []
        for line in fp:
            report = [int(x) for x in line.strip().split()]
            reports.append(report)
    global_result = 0
    for report in reports:
        level = 0
        # binomial coefficients
        coeffs = [1]
        # drill down until zero
        i = 0
        while True:
            alternated_coeffs = alternate(coeffs)
            zipped = list(zip(reversed(alternated_coeffs), report[i : i + level + 1]))
            z = sum([x * y for x, y in zipped])
            if z != 0:
                i = 0
                level += 1
                coeffs = next_coeffs(coeffs)
            else:
                i += 1
                if i + level == len(report):
                    break
        # we have found a level with all zeroes
        # we can now compute the rightmost diagonal
        coeffs = [1]
        result = 0
        for _ in range(level):
            alternated_coeffs = alternate(coeffs)
            zipped = list(zip(reversed(alternated_coeffs), report[-len(coeffs) :]))
            z = sum([x * y for x, y in zipped])
            result += z
            coeffs = next_coeffs(coeffs)
        global_result += result
    print(global_result)


if __name__ == "__main__":
    main()
