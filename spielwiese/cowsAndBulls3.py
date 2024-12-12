import random
import numpy as np


def GetNumbers(maxNumbers):
    numlist = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    numbers = random.sample(numlist, maxNumbers)
    return numbers


def CompareNumbers(guessedNum, searchedNum):
    cow = 0
    bull = 0

    for i in range(len(searchedNum)):
        if (guessedNum[i] == searchedNum[i]):
            bull += 1
        else:
            if guessedNum[i] in searchedNum:
                cow += 1
    return cow, bull


def CheckInput(searchedNum, guessedNum):
    if len(guessedNum) != len(searchedNum):
        print("Bitte geben Sie", len(searchedNum), "Zahlen ein.")
        return False
    elif len(set(guessedNum)) != len(searchedNum):
        print("Es sind keine doppelten Zahlen erlaubt.")
        return False
    else:
        return True


if __name__ == "__main__":
    maxNumbers = 4
    while True:
        countDigits = int(input("Wieviel Zahlen wollen Sie raten? "))

        if(countDigits > maxNumbers):
            print(f"Sie können max. {maxNumbers} Zahlen raten.")
        else:
            searchedNumber = GetNumbers(countDigits)
            # print(searchedNumber)
            break

    counter = 0
    guessedNumberStr = ""
    while True:
        counter += 1
        guessedNumber = list(str(input("> ")))
        if CheckInput(searchedNumber, guessedNumber):
            cow, bull = CompareNumbers(guessedNumber, searchedNumber)
            if bull == countDigits:
                print(
                    f"Prima, die gesuchte Zahl {guessedNumberStr.join(guessedNumber)} ist richtig. Versuche: {counter}")
                break
            else:
                print(f"cow: {cow}, bull: {bull}")
