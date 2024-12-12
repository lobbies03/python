sinputValues = [12, 35, 9, 56, 24, 38]


def changeFirstWithLastListElement(values):
    if (len(values) > 1):
        firstValue = values[0]
        lastValue = values[-1]
        values[0] = lastValue
        values[-1] = firstValue

    return values


print(inputValues)
print(changeFirstWithLastListElement(inputValues))
