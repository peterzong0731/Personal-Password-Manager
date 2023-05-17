from random import SystemRandom

# All possible characters in a password
lowercaseLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
uppercaseLetters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
specialSymbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', ',', '.', '?', '[', ']', '{', '}']

# Cryptographically secure randomizer
sys_random = SystemRandom()

def generatePassword(length, includeSymbols, includeNumbers):
    password = []

    # Passwords must be at least 4 characters long
    if length < 4:
        print("Error")
        return -1

    remainingChars = length

    # If the password will contain numbers
    if includeNumbers:
        numNumbers = sys_random.randint(1, length // 2.5)
        # If the password will contain numbers and symbols
        if includeSymbols:
            numSymbols = min(sys_random.randint(1, length // 2.5), length - 3)
            remainingChars -= numSymbols
            randSymbols = sys_random.choices(specialSymbols, k = numSymbols)
            password = randSymbols

            numNumbers = min(numNumbers, remainingChars - 2)


        remainingChars -= numNumbers
        password += sys_random.choices(numbers, k = numNumbers)
        
        numUppercase = sys_random.randint(1, remainingChars - 1)
        remainingChars -= numUppercase

    # If the password will contain symbols but not numbers
    elif includeSymbols:
        numSymbols = min(sys_random.randint(1, length // 2.5), length - 2)
        remainingChars -= numSymbols
        randSymbols = sys_random.choices(specialSymbols, k = numSymbols)
        password = randSymbols

        numUppercase = sys_random.randint(1, remainingChars - 1)
        remainingChars -= numUppercase

    # If the password will only contain letters
    else:
        numUppercase = sys_random.randint(1, length - 1)
        remainingChars -= numUppercase

    # Choose uppercase letters
    password += sys_random.choices(uppercaseLetters, k = numUppercase)
    # Choose lowercase letters
    password += sys_random.choices(lowercaseLetters, k = remainingChars)

    # Shuffle the password order (in place)
    sys_random.shuffle(password)

    # If there is a length mismatch, which should not happen
    if (len(password) != length):
        print ("Error length mismatch: " + str(len(password)) + " v.s. " + str(length))

    # Return the password as a string
    return ''.join(password)



if __name__ == "__main__":
    count = 3
    turn = 0
    while(count < 20):
        l = count
        print(generatePassword(l, True, True))
        print(generatePassword(l, True, False))
        print(generatePassword(l, False, True))
        print(generatePassword(l, False, False))

        print()
        turn += 1
        if turn == 4:
            count += 1
            turn = 0