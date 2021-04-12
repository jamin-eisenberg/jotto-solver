from json import load
import collections
from z3 import Int

# Iterative binary search
# Returns the index of the element in the list if present, otherwise -1
def binary_search(x, ls):
    low = 0
    high = len(ls) - 1
    mid = 0
 
    while low <= high:
 
        mid = low + (high - low) // 2
 
        if ls[mid] < x:
            low = mid + 1
 
        elif ls[mid] > x:
            high = mid - 1
 
        else:
            return mid
 
    return -1

# loads a list of words in from a file with the given name
# loads a mapping of guesses to their match number from a file with the given name
# filters the list of words to make them all the length of the given number of letters
# makes sure all of the guesses are in the list of words
# returns a tuple of the list of words and the dictionary of guesses
def get_allwords_and_guesses(allwords_fd, guesses_fd, sw_letters):
    
    with open(allwords_fd) as allwords_f:
        with open(guesses_fd) as guesses_f:
            allwords = sorted(allwords_f.readlines())
            guesses = load(guesses_f)
            

    allwords = list(map(lambda s: s.strip(), allwords))
    allwords = list(filter(lambda s: len(s) == sw_letters, allwords))

    for i, s in enumerate(allwords):
        allwords[i] = str_to_list_nums(s)

    for guess in guesses:
        if binary_search(str_to_list_nums(guess), allwords) == -1:
            raise ValueError("All guesses must be in the provided dictionary"
                             "and the same length as the secret word. "
                             f"'{guess}' violates this.")

    return allwords, guesses

# converts each letter in a string to a number according to get_num_from_char
def str_to_list_nums(s):
    return list(map(lambda ch: get_num_from_char(ch), s))

# converts a number from 0 to 25 to a letter from 'a' to 'z'
def get_char_from_num(n):
    if 0 <= n <= 25:
        return chr(n + 97)
    raise ValueError("Can only convert numbers between 0 and 25.")

# converts a letter from 'a' to 'z' to a number from 0 to 25
def get_num_from_char(ch):
    n = ord(ch) - 97
    if 0 <= n <= 25:
        return n
    raise ValueError("Can only convert letters between 'a' and 'z'.")



def main(allwords_fd, guesses_fd, sw_letters):
    allwords, guesses = get_allwords_and_guesses(allwords_fd, guesses_fd, sw_letters)

    secret_word = [ Int(f"letter_{i}") for i in range(sw_letters) ]

    # all of secret_word's letters must be between 'a' and 'z'

    # secret_word must be in the dictionary

    # for each guess:
    #    matchNumber(guess, secret_word) must be the guess's given number of matches


if __name__ == '__main__':

    main("exampleWords.txt", "example.txt", 4)

##     sw_letters = int(input("Enter the number of letters in the secret word: "))
##    main(
##        input("Enter the filename you want to load the dictionary of words from: "),
##        input("Enter the filename you want to load the history of guesses from: "),
##        sw_letters)


