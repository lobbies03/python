import random
import os

os.system('clear')

anz = int(input("Wieviel Aufgaben möchtest Du lösen? "))
cnt = 0
cntErr = 0

while (cnt < anz):
    z1 = random.randint(1, 9)
    z2 = random.randint(1, 9)
    res = z1*z2
    inpStr = str(z1) + " x " + str(z2) + " = "
    inp = input(inpStr)
    inpStr = inpStr + str(res)

    if (res != inp):
        cntErr += 1
        print(inpStr)

    cnt += 1

print("Es waren {:d} von {:d} Aufgaben richtig.".format(anz-cntErr, anz))
