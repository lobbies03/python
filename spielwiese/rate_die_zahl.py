import random
import os

os.system('clear')


def rateDieZahl():
    gesuchteZahl = random.randint(1, 24)
    retryCounter = 0
    while 1:
        retryCounter = retryCounter + 1
        eingabeZahl = int(input("Rate eine Zahl zwischen 0 und 25: "))
        if eingabeZahl > gesuchteZahl:
            print("Ihre Zahl ist zu groß. Nochmal raten...")
        elif eingabeZahl < gesuchteZahl:
            print("Ihre Zahl ist zu klein. Nochmal raten!")
        else:
            print("Richtig, sie benötigten", retryCounter, "Versuche")
            break


rateDieZahl()
