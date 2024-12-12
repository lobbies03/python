import random

a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

a = random.sample(range(10, 30), 5)
b = random.sample(range(10, 30), 7)

commonElem = []
for listA in a:
    for listB in b:
        if listA == listB:
            if not listA in commonElem:
                commonElem.append(listA)
print(a)
print(b)
print(commonElem)
