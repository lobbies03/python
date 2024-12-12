import random

a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

a = random.sample(range(100), 10)
b = random.sample(range(100), 13)

print(a)
print(b)
duplicates = [x for x in a if x in b]
print(duplicates)
