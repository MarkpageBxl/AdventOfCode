#!/usr/bin/env python

safe_reports = 0


def compute_slice_safety(levels: list[int]) -> bool:
    for i in range(len(levels)):
        slice = levels[:]
        del slice[i]
        if compute_safety(slice):
            return True
    return False


def compute_safety(levels: list[int]) -> bool:
    consistent_delta_sign = True
    safe_distance = True
    increasing = levels[0] < levels[1]
    i = 0

    while i < len(levels) - 1:
        if (levels[i] < levels[i + 1]) != increasing:
            consistent_delta_sign = False
            break
        elif not (1 <= abs(levels[i + 1] - levels[i]) <= 3):
            safe_distance = False
            break
        i += 1
    return consistent_delta_sign and safe_distance


with open("input") as fp:
    for line in fp:
        levels = [int(x) for x in line.strip().split()]
        if compute_safety(levels) or compute_slice_safety(levels):
            safe_reports += 1
            continue


print(safe_reports)
