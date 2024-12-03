#!/usr/bin/env python

import re

MUL_RE = re.compile(r"mul\(([0-9]+),([0-9]+)\)|(do)\(\)|(don't)\(\)")

result = 0
enabled = True
with open("input") as fp:
    for line in fp:
        matches = MUL_RE.findall(line)
        for i1, i2, do, dont in matches:
            if enabled and i1 and i2:
                result += int(i1) * int(i2)
            elif do:
                enabled = True
            elif dont:
                enabled = False

print(result)
