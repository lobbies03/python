file = "bunchOfNames.txt"
names = {}

with open(file, "r") as stream:
    line = stream.readline()
    while line:
        line = line.strip()
        if line in names:
            names[line] += 1
        else:
            names[line] = 1
        line = stream.readline()

print(names)
