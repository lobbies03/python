import random


def GetNumbers(maxNumbers):
    numlist = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    numbers = random.sample(numlist, maxNumbers)
    # return ''.join(numbers)
    return numbers


def CompareNumbers(inputNumbers, searchedNumbers):
    cowBull = [0, 0]
    for i in range(len(searchedNumbers)):
        if inputNumbers[i] == searchedNumbers[i]:
            cowBull[1] += 1
        else:
            for j in range(i, len(searchedNumbers)):
                if not i == j:
                    if inputNumbers[j] == searchedNumbers[j]:
                        cowBull[0] += 1
    return cowBull


if __name__ == "__main__":
    # maxNumbers = int(input("Wieviel Nummern möchtest du raten? "))
    maxNumbers = 4
    searchedNumbers = GetNumbers(maxNumbers)
    print(searchedNumbers)
    while True:
        inputNumbers = str(input("> "))
        if len(inputNumbers) != len(searchedNumbers):
            print(f"Es wird nach {len(searchedNumbers)}-Stellen gesucht.")
        elif inputNumbers == searchedNumbers:
            print(f"Prima, die Zahl {inputNumbers} ist korrekt.")
            break
        else:
            result = CompareNumbers(inputNumbers, searchedNumbers)
            print(result)
