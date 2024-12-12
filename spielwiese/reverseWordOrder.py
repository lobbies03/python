def ReverseOrder(words):
    result = words.split(" ")
    newOrder = []
    # b = []
    # b = [a for a in result.range(words.size(), 0)]
    for word in range(len(result), 0, -1):
        newOrder.append(result[word-1])
    join = " ".join(newOrder)
    return join


def ReverseOrderV2(x):
    y = x.split()
    return " ".join(y[::-1])


def ReverseOrderV3(x):
    y = x.split()
    return " ".join(reversed(y))


a = "My name is Michele"

print(a)
print(ReverseOrder(a))

print(a)
print(ReverseOrderV2(a))

print(a)
print(ReverseOrderV3(a))
