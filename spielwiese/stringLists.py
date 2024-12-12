inp = str(input("Bitte geben Sie ein Wort ein: ")).lower()
revInp = inp[::-1]

if inp == revInp:
    print(f"{inp} ist ein Palindrome")
else:
    print(f"{inp} ist kein Palindrome")
