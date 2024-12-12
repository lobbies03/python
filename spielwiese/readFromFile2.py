file = "bunchOfNames2.txt"
names = {}

with open(file, "r") as stream:
    lines = stream.read().splitlines()
    fileCounter = 0
    for line in lines:
        category = ""
        numberOfFiles = 0
        length = len(line)
        index = len(line)

        for c in line[::-1]:
            if c == "/":
                category = line[0:index]
                if category in names:
                    names[category] += 1
                    break
                else:
                    names[category] = 1
                    break

            index -= 1

for k, v in names.items():
    print(k, v)
