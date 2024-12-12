# /3: Fizz
# /5: Buzz
# /3/5: FizzBuzz
# any ohter number show input

def fizz_buzz(input):
    if (input % 3 == 0 and input % 5 == 0):
        return "FizzBuzz"
    if (input % 3 == 0):
        return "Fizz"
    if (input % 5 == 0):
        return "Buzz"

    return input


print(fizz_buzz(1))
