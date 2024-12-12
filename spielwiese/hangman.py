import random


def GetWordsFromTxtFile(filename):
    with open(filename, "r") as f:
        line = f.readline().strip()
        words.append(line)
        while line:
            words.append(line)
            line = f.readline().strip()

    return words


def GuessWord(lettersList, guessedWord):
    word = ""
    correctLetter = 0
    for letter in guessedWord:
        if letter in lettersList:
            correctLetter+=1
            word = word + letter + " "
        else:
            word = word + "_ "
    print(f"{word} ({len(guessedWord)})")


if __name__ == "__main__":

    words = []
    words = GetWordsFromTxtFile("sowpods.txt")
    rNum = random.randint(0, len(words))
    wordToGuess = words[rNum]
    print("Willkommen zu Hangman. Sie haben 6 Versuche um das Wort zu erraten. Viel Spaß!")
    print(wordToGuess)

    maxIncorrectLetters = 6
    countIncorrectLetters = 0
    counter = 0
    lettersList = []
    GuessWord(lettersList, wordToGuess)
    while(counter < maxIncorrectLetters):
        letter = input("Buchstabe: ").upper()

        lettersList.append(letter)
        GuessWord(lettersList, wordToGuess)
        counter += 1
