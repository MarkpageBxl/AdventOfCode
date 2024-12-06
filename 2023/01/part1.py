#!/usr/bin/env python

total = 0
with open("input") as fp:
    for line in fp:
        digits = [x for x in line if x.isdigit()]
        print(digits)
        value = int(digits[0] + digits[-1])
        total += value

print(total)