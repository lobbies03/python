import random
import os

os.system('clear')


def GeneriereLottzahlen():
    zahlen = []
    anzZahlen = 6
    while True:
        zahl = random.randint(1, 49)
        if not zahl in zahlen:
            zahlen.append(zahl)
        if len(zahlen) == anzZahlen:
            zahlen.sort()
            for i in range(anzZahlen):
                print(f"{i+1}.Zahl: {zahlen[i]}")
            break

def GeneriereZusatzSuper():
    zahl = random.randint(0, 9)
    print("Superzahl:", zahl)


GeneriereLottzahlen()
GeneriereZusatzSuper()
