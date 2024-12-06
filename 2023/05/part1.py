#!/usr/bin/env python
#
# Solution for Advent of Code 2023
# Day 5, part 1
#
# Challenge URL: https://adventofcode.com/2023/day/5
#
# Author: Markus Lindström <markus@markpage.be>
#


def map_id(id: int, mappers: list[tuple[int, int, int]]) -> int:
    mapped_id = id
    for mapper in mappers:
        dst, src, range = mapper
        if src <= id < src + range:
            mapped_id = dst + (id - src)
            break
    return mapped_id


converters: dict[(str, str), list[str]] = {}

with open("input") as fp:
    # seeds
    line = next(fp).strip()
    seeds = [int(x) for x in line[len("seeds :") :].split()]
    next(fp)
    try:
        while True:
            src_category, dst_category = next(fp)[:-6].split("-to-")
            mappers = []
            while (record := next(fp).strip()) != "":
                mappers.append(tuple([int(x) for x in record.split()]))
            converters[(src_category, dst_category)] = mappers
    except StopIteration:
        pass
    finally:
        converters[(src_category, dst_category)] = mappers

locations = []
for current_id in seeds:
    for type, mappers in converters.items():
        dst_id = map_id(current_id, mappers)
        current_id = dst_id
    locations.append(current_id)

print(locations)
print(min(locations))
