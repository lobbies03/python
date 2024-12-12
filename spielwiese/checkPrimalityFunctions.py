def GetNumber():
    return int(input("Bitte geben Sie eine Zahl ein: "))


def CheckPrime(num):
    prime = True
    divisor = []
    for i in range(2, num):
        if num % i == 0:
            divisor.append(i)
            prime = False
    return prime, divisor


number = GetNumber()
prime, divisor = CheckPrime(number)

if prime:
    print(f"Die Zahl {number} ist eine Primzahl.")
else:
    print(f"Die Zahl {number} ist keine Primzahl. Teiler sind {divisor}")
