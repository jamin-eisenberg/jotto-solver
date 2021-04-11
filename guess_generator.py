from json import dump

guesses = {}

while True:
    currGuess = input("Enter the guess, or enter 's' save the file, and 'q' to quit: ")

    if(currGuess == 'q'):
        quit()
    elif(currGuess == 's'):
        fd = input("Enter a full filename to save this set of guesses to: ")
        with open(fd, 'w') as outfile:
            dump(guesses, outfile)
        quit()
    else:
        matchNumber = int(input("How many letters in the guess match the secret word? "))
        guesses[currGuess] = matchNumber

