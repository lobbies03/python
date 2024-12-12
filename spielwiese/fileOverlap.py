def readFileInList(filename):
    numList = []
    with open(filename, "r") as s1:
        line = s1.readline()
        while line:
            numList.append(line.strip())
            line = s1.readline()

    return numList


f1 = "primeNumbers.txt"
f2 = "happyNumbers.txt"
lst1 = readFileInList(f1)
lst2 = readFileInList(f2)

duplicates = [x for x in lst1 if x in lst2]
print(duplicates)
