num = int(input("Bitte Zahl eingeben: "))
check = int(input("Bitte Divisor eingeben: "))

if num % 4 == 0:
    print("Zahl durch 4 teilbar")
else:
    if num % 2 == 0:
        print("gerade")
    else:
        print("ungerade")

if num % check == 0:
    print(
        f"Die Zahl {num} lässt sich durch {check} teilen. Ergebnis: {num/check}")
else:
    print(f"Ergebnis keine natürliche Zahl {num/check}")
