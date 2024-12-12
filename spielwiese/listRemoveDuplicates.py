def RemoveDuplicates(valueList):
    newList = []
    for i in valueList:
        if not i in newList:
            newList.append(i)
    newList.sort()
    return newList

def RemoveDuplicatesWtihSet(valueList):
    return set(valueList)

a = [1, 2, 5, 1, 4, 2, 1, 3, 4, 5]

print(RemoveDuplicates(a))
print(RemoveDuplicatesWtihSet(a))
