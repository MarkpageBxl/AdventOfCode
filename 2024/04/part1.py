#!/usr/bin/env python

PATTERN = "XMAS"

count = 0

with open("input") as fp:
    data = [line.strip() for line in fp]

# horizontal search
for line in data:
    count += line.count(PATTERN)
    count += line.count(PATTERN[::-1])
print("after horizontal search:", count)

# vertical search
scope = []
for column in range(len(data[0])):
    col_data = ""
    for line in data:
        col_data += line[column]
    scope.append(col_data)

for line in scope:
    count += line.count(PATTERN)
    count += line.count(PATTERN[::-1])

print("after vertical search:", count)

# diagonal search 1
# 2n - 1 diagonals in a n x n matrix
dimension = len(data)
scope = []

# top half sweep, left to right
for n in range(dimension):
    diag = ""
    for k in range(dimension - n):
        diag += data[n + k][k]
    count += diag.count(PATTERN)
    count += diag.count(PATTERN[::-1])

print("after diagonal top sweep LR search:", count)

# bottom half sweep, left to right, skip first diagonal (duplicate)
for n in range(1, dimension):
    diag = ""
    for k in range(dimension - n):
        diag += data[k][n + k]
    count += diag.count(PATTERN)
    count += diag.count(PATTERN[::-1])

print("after diagonal bottom sweep LR search:", count)

# top half sweep, right to left
scope = []
for n in range(dimension):
    diag = ""
    for k in range(n + 1):
        diag += data[k][n - k]
    scope.append(diag)
    count += diag.count(PATTERN)
    count += diag.count(PATTERN[::-1])

print("after diagonal top sweep RL search:", count)

# bottom half sweep, right to left, skip first diagonal (duplicate)
scope = []
for n in range(dimension - 1):
    diag = ""
    for k in range(n + 1):
        diag += data[dimension - 1 - n + k][dimension - 1 - k]
    scope.append(diag)
    count += diag.count(PATTERN)
    count += diag.count(PATTERN[::-1])

print("after diagonal bottom sweep RL search:", count)

print("total:", count)
