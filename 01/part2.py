l1 = []
l2 = []

# data load
with open("input") as fp:
    for line in fp:
        left, right = line.strip().split()
        i1, i2 = int(left), int(right)
        l1.append(i1)
        l2.append(i2)

similarity_score = 0

for i in l1:
    count = len([j for j in l2 if j == i])
    similarity_score += i * count

print(similarity_score)
