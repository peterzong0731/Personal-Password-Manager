import pandas as pd
from random import SystemRandom

lowercaseLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
uppercaseLetters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
specialSymbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', ',', '.', '?']

sys_random = SystemRandom()


length = 8
includeSymbols = False
includeNumbers = True
password = ''

if length < 4:
    print("Error")

if includeNumbers:
    if includeSymbols:
        numSymbols = sys_random.randint(1, length // 3)
        randSymbols = sys_random.choices(specialSymbols, k = numSymbols)
    else:
        pass

elif includeSymbols:
    pass
else:
    password = sys_random.choices(lowercaseLetters + uppercaseLetters + numbers + specialSymbols, k = length)

print(''.join(password))