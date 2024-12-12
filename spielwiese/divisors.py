# https://www.practicepython.org/xercise/2014/02/26/04-divisors.html

num = int(input("Bitte Zahl eingeben: "))
divisors = []
for i in range(1, num+1):
    if num % i == 0:
        divisors.append(i)
print(divisors)
