import random

a = [5, 10, 15, 20, 25]


def GetFirstLastNumber(listOfNumbers):
    return [listOfNumbers[0], listOfNumbers[-1]]


print(GetFirstLastNumber(a))
