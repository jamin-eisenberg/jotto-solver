from json import dump

guesses = {}

word_length = int(input("How many letters is the secret word? "))

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

        if len(set(currGuess)) < len(currGuess) or len(currGuess) != word_length:
            print("Guesses cannot have duplicate letters and they must be the same length as the secret word. Please try again.")
            continue

        matchNumber = int(input("How many letters in the guess match the secret word? "))
        guesses[currGuess] = matchNumber

