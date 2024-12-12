import random
import time
import os
import datetime

addition = "1"
subtraktion = "2"
multiplikation = "3"
division = "4"

Spieler = {
    "1": "Mika",
    "2": "Finn",
    "3": "Mama",
    "4": "Papa"
}
os.system('clear')


def Aufgabe(zahl1, zahl2, rechenart):
    tic = time.perf_counter()

    if rechenart == addition:
        aufgabe = str(zahl1) + "+" + str(zahl2) + "="
        erg = Eingabe(aufgabe)
        erg1 = zahl1 + zahl2
    elif rechenart == subtraktion:
        aufgabe = str(zahl1) + "-" + str(zahl2) + "="
        erg = Eingabe(aufgabe)
        erg1 = zahl1 - zahl2
    elif rechenart == multiplikation:
        aufgabe = str(zahl1) + "x" + str(zahl2) + "="
        erg = Eingabe(aufgabe)
        erg1 = zahl1 * zahl2
    elif rechenart == division:
        aufgabe = str(zahl1) + ":" + str(zahl2) + "="
        erg = Eingabe(aufgabe)
        erg1 = int(zahl1 / zahl2)

    toc = time.perf_counter()

    timeElapsed = toc - tic
    # print(f"Zeit: {toc-tic:0.4f} Sekunden")

    if erg != erg1:
        print("Leider falsch, richtig wäre", erg1)
        ergebnis = False
    else:
        ergebnis = True

    WriteToFile(aufgabe + str(erg) + "," + str(ergebnis) +
                "," + str(timeElapsed.__round__(1)))

    return ergebnis


def WriteToFile(text):
    x = datetime.datetime.now()
    filename = x.strftime("%Y-%m-%d")
    # print(filename)

    with open(filename, "a") as f:
        f.write(text + "\r\n")
        f.close


def Eingabe(aufgabe):
    return int(input(aufgabe))


# print("(1) Mika")
# print("(2) Finn")
# spieler = input("Spieler wählen? ")
os.system('clear')

print("(1) Addition       (+)")
print("(2) Subtraktion    (-)")
print("(3) Multiplikation (*)")
print("(4) Division       (:)")

rechenart = input("Rechenart wählen? ")
os.system('clear')
anzahl = int(input("Wieviele Aufgaben wollen Sie lösen? "))
os.system('clear')

zähler = 0
zählerFalsch = 0
while zähler < anzahl:
    if rechenart == addition:
        z1 = random.randint(1, 100)
        z2 = random.randint(1, 100)
        ergebnis = Aufgabe(z1, z2, rechenart)

    if rechenart == subtraktion:
        while 1:
            z1 = random.randint(0, 100)
            z2 = random.randint(0, 100)
            if z1 > z2:
                ergebnis = Aufgabe(z1, z2, rechenart)
                break

    if rechenart == multiplikation:
        z1 = random.randint(0, 10)
        z2 = random.randint(0, 10)
        ergebnis = Aufgabe(z1, z2, rechenart)

    if rechenart == division:
        z1 = random.randint(1, 10)
        z2 = random.randint(1, 10)
        e1 = z1 * z2
        z1 = e1
        ergebnis = Aufgabe(z1, z2, rechenart)

    if ergebnis == False:
        zählerFalsch = zählerFalsch + 1

    zähler = zähler + 1

print("Sie haben " + str(anzahl-zählerFalsch) +
      " von " + str(anzahl) + " richtig gelöst.")

# eingabe = input("Nochmal spielen? (ja/nein) ")
# if eingabe != "j":
#     quit
