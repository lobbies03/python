import random

words = []


def GetWordsFromTxtFile(filename):

    with open(filename, "r") as f:
        line = f.readline().strip()
        words.append(line)
        while line:
            words.append(line)
            line = f.readline().strip()

    return words


words = GetWordsFromTxtFile("sowpods.txt")
rNum = random.randint(0, len(words))
print(words[rNum])
