#!/usr/bin/env python
#
# Solution for Advent of Code 2023
# Day 5, part 2
#
# Challenge URL: https://adventofcode.com/2023/day/5#part2
#
# Author: Markus Lindström <markus@markpage.be>
#

from typing import Optional


def get_seed_intervals(seeds: list[int]) -> list[tuple[int, int]]:
    intervals = []
    for i in range(0, len(seeds), 2):
        intervals.append((seeds[i], seeds[i + 1]))
    return intervals


def rel_to_abs(rel_interval: Optional[tuple[int, int]]) -> Optional[tuple[int, int]]:
    if not rel_interval:
        return None
    return (rel_interval[0], rel_interval[0] + rel_interval[1] - 1)


def abs_to_rel(abs_interval: Optional[tuple[int, int]]) -> Optional[tuple[int, int]]:
    if not abs_interval:
        return None
    return (abs_interval[0], abs_interval[1] - abs_interval[0] + 1)


def compute_interval_overlap(
    rel1: tuple[int, int], rel2: tuple[int, int]
) -> tuple[Optional[tuple[int, int]], list[tuple[int, int]]]:
    overlap = None
    non_overlap = []
    d1, d2 = [rel_to_abs(x) for x in (rel1, rel2)]
    if d1[1] < d2[0] or d2[1] < d1[0]:
        # full disjunction
        overlap = None
        non_overlap = [d1]
    elif d1[0] < d2[0] and d2[0] <= d1[1] <= d2[1]:
        # partial overlap (left)
        non_overlap.append((d1[0], d2[0] - 1))
        overlap = (d2[0], d1[1])
    elif d2[0] <= d1[0] <= d2[1] and d1[1] > d2[1]:
        # partial overlap (right)
        overlap = (d1[0], d2[1])
        non_overlap.append((d2[1] + 1, d1[1]))
    elif d1[0] >= d2[0] and d2[1] <= d2[1]:
        # d1 subset of d2
        overlap = d1
        non_overlap = []
    elif d1[0] < d2[0] and d1[1] > d2[1]:
        # d1 superset of d2
        overlap = d2
        non_overlap.append((d1[0], d2[0] - 1))
        non_overlap.append((d2[1] + 1, d1[1]))
    else:
        assert False

    non_overlap = [abs_to_rel(x) for x in non_overlap]
    overlap = abs_to_rel(overlap)

    return overlap, non_overlap


def compute_destination_intervals(
    src_intervals: list[tuple[int, int]], mapper: list[tuple[int, int, int]]
) -> list[tuple[int, int]]:
    result = []
    intervals_to_handle = set(src_intervals)
    while len(intervals_to_handle) > 0:
        intervals_to_check = {intervals_to_handle.pop()}
        for rule in mapper:
            dst_base, src_base, _ = rule
            next_round_intervals = set()
            for interval in intervals_to_check:
                overlap, non_overlapping = compute_interval_overlap(interval, rule[1:])
                # Keep track of non overlapping intervals
                next_round_intervals.update(non_overlapping)
                # Rebase overlapping interval
                if overlap:
                    rebased_overlap = (overlap[0] - src_base + dst_base, overlap[1])
                    result.append(rebased_overlap)
            intervals_to_check = next_round_intervals
        # All rules exhausted. Remaining intervals kept as is.
        result.extend(intervals_to_check)
    return result


def main():
    mappers: dict[(str, str), list[str]] = {}
    with open("input") as fp:
        line = next(fp).strip()
        seeds = [int(x) for x in line[len("seeds :") :].split()]
        seed_intervals = get_seed_intervals(seeds)
        next(fp)
        try:
            while True:
                mapper_name = next(fp)[:-6]
                rules = []
                while (record := next(fp).strip()) != "":
                    rules.append(tuple([int(x) for x in record.split()]))
                mappers[mapper_name] = rules
        except StopIteration:
            pass
        finally:
            mappers[mapper_name] = rules

    locations = []
    intervals = seed_intervals
    for _, mapper in mappers.items():
        intervals = compute_destination_intervals(intervals, mapper)
        pass

    base_locations = [x[0] for x in intervals]
    print(min(base_locations))


if __name__ == "__main__":
    main()
