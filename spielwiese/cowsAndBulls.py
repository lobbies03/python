import random


def GetRandomDigit():
    return random.randint(0, 9)


def CompareNumbers(value, searched):
    bull = 0
    cow = 0
    textCow = "cow"
    textBull = "bull"

    if value == searched:
        print(f"Prima, die Zahl {searched} ist richtig!")
        return True
    elif len(value) != len(searched):
        print(
            f"Ihre Zahl hat {len(value)}-Stellen, gesucht ist eine Zahl mit {len(searched)}-Stellen.")
    else:
        for i in range(len(searched)):
            if value[i] == searched[i]:
                bull += 1
            else:
                j = i+1
                for j in range(len(searched)):
                    if value[i] == searched[j]:
                        cow += 1
        if cow > 1:
            textCow = "cows"

        if bull > 1:
            textBull = "bulls"
    print(f"{cow} {textCow}, {bull} {textBull}")


def CompareNumbers2(numbers):
    if numbers[0] == numbers[1]:
        cowbul = [0, 1]
    else:
        cowbul = [1, 0]
    return cowbul


if __name__ == "__main__":
    numberOfDigits = 5
    numberOfDigits = int(input("Wieviel Stellen soll ihre Zahl haben? "))
    searchValue = ""
    for i in range(numberOfDigits):
        searchValue += str(GetRandomDigit())
    # print(searchValue)
    print(f"Bitte raten Sie die {numberOfDigits}-stellige Zahl?")

    while True:
        value = str(input(">"))
        cowbul = [0, 0]

        for i in range(0,numberOfDigits):
            CompareNumbers(value, searchValue)
            break
