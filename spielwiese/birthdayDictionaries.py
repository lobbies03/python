birthDict = {
    "Michael Hahn": "27.11.1973",
    "Sophia Hollander": "22.11.1979",
    "Mika Hahn": "02.08.2011",
    "Finn Hahn": "30.11.2012"
}

print('Willkommen zu dem Geburtstags Dictionary. Wir wissen die Geburtstage der Familie:')
for name in birthDict:
    print(name)

print()
name = input("Von wem möchten Sie den Geburtstag wissen? ")
if name in birthDict:
    print("{}'s Geburstag ist am {}".format(name, birthDict[name]))
else:
    print("Tut mir leid, {}'s Geburtstag ist nicht vorhanden.".format(name))
