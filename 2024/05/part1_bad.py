#!/usr/bin/env python
#
# Solution for Advent of Code 2024
# Day 5, part 1
#
# Challenge URL: https://adventofcode.com/2024/day/5
#
# Author: Markus Lindström <markus@markpage.be>
#

# Bad approach. Turns out the ruleset is not a DAG!

import graphlib
from collections import defaultdict


def write_graphviz(rules):
    with open("graph.dot", "w") as fp:
        fp.write("digraph G {\n")
        fp.write("rankdir LR;\n")
        for rule in rules:
            fp.write(f"{rule[0]} -> {rule[1]};\n")
        fp.write("}\n")


graph = defaultdict(list)

rules = set()
updates: list[list[int]] = []
with open("input") as fp:
    rule_mode = True
    for line in fp:
        if not line.strip():
            rule_mode = False
            continue
        if rule_mode:
            s = [x for x in line.strip().split("|")]
            s[0] = int(s[0])
            s[1] = int(s[1])
            rules.add(tuple(s))
        else:
            updates.append([int(x) for x in line.strip().split(",")])

# output grahviz
write_graphviz(rules)

# build graph for topological sort
for rule in rules:
    source, target = rule
    graph[target].append(source)

print(graph)

# topological sort
ts = graphlib.TopologicalSorter(graph)
order = tuple(ts.static_order())
print(order)

# create dict to help with order comparison
order_dict: dict[int, int] = {x: i for i, x in enumerate(order)}
print(order_dict)

correct_updates = []
middle_pages = 0
for update in updates:
    sorted_update = update[:]
    sorted_update.sort(key=lambda x: order_dict[x])
    if update == sorted_update:
        correct_updates.append(update)
        assert len(update) % 2 == 1
        middle_pages += update[len(update)//2]

print(middle_pages)