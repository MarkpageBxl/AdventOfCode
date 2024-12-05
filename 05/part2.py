#!/usr/bin/env python

from collections import defaultdict

rules = defaultdict(list)
updates: list[list[int]] = []
with open("input") as fp:
    rule_mode = True
    for line in fp:
        if not line.strip():
            rule_mode = False
            continue
        if rule_mode:
            s = [x for x in line.strip().split("|")]
            dependency = int(s[0])
            target = int(s[1])
            rules[target].append(dependency)
        else:
            updates.append([int(x) for x in line.strip().split(",")])

bad_updates = []
for update in updates:
    valid = True
    for i in range(len(update) - 1):
        if update[i] not in rules[update[i + 1]]:
            valid = False
            bad_updates.append(update)
            break


def compare_pages(i: int, j: int, rules: dict[int, int]) -> int:
    if i == j:
        assert False
    if i in rules[j]:
        # i is a dependency of j, must be before => i < j
        return -1
    if j in rules[i]:
        # i depends on j, must be after => i > j
        return 1
    assert False


middle_pages = 0
for update in bad_updates:
    # selection sort
    for i in range(len(update) - 1):
        for j in range(i + 1, len(update)):
            if compare_pages(update[i], update[j], rules) > 0:
                update[i], update[j] = update[j], update[i]
    middle_pages += update[len(update) // 2]

print(middle_pages)
