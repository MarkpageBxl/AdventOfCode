import re

MUL_RE = re.compile(r"mul\(([0-9]+),([0-9]+)\)")

result = 0
with open("input") as fp:
    for line in fp:
        matches = MUL_RE.findall(line)
        for a, b in matches:
            result += int(a) * int(b)

print(result)
