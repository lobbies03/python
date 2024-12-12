def GetFibonacci(amountOfNumbers):
    fibo = []
    for n in range(amountOfNumbers):
        if n < 2:
            fibo.append(1)
        else:
            fibo.append(fibo[n-1] + fibo[n-2])
    return fibo


inp = int(input("Bitte Anzahl an Fibonacci Nummern eingeben: "))
print(GetFibonacci(inp))
