import unittest

def sum(number):
    if number < 10:
        print(number)
        sum(number+1)

sum(1)

