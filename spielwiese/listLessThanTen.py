a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
num = int(input("Bitte Zahl eingeben: "))

newList = []
for elem in a:
    if elem < num:
        newList.append(elem)
print(newList)
