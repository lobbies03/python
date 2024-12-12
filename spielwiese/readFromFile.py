file = "bunchOfNames.txt"
names = {}

with open(file, "r") as stream:
    lines = stream.read().splitlines()
    for line in lines:
        if line in names:
            value = names.get(line)
            value +=1
            names[line] = value
        else:
            names[line] = 1
            names[line] = 1

for k, v in names.items():
    print(k, v)

