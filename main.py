from json import load
import collections
from z3 import *

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
            high = mid -1 
        else:
            return mid
 
    return -1

# generates a constraint for the given number being in the list of numbers
def num_in_list_z3(x, ls):
    if ls == []:
        return False
    return Or(x == ls[0], num_in_list_z3(x, ls[1:]))

# generates a constraint for list equality between the given lists
def list_equal_z3(ls1, ls2):
    if ls1 == [] or ls2 == []:
        return ls1 == ls2
    return And(ls1[0] == ls2[0], list_equal_z3(ls1[1:], ls2[1:]))

# generates a constraint for making x, a list of numbers, in a list of list of numbers
def list_in_lol_z3(x, ls):
    if ls == []:
        return False
    return Or(list_equal_z3(x, ls[0]), list_in_lol_z3(x, ls[1:]))



# returns a tuple with:
#   a list of list of numbers 0-25 representing words loaded from a file with the given name
#   a mapping of guesses to their match number loaded from a file with the given name
# the list of words is sorted and filtered to only include words of the given length
# the list of words is converted into a list of list of numbers 0-25
# the mapping of guesses is verified to make sure all guesses are in the dictionary
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
    return list(map(lambda ch: char_to_num(ch), s))

# converts a list of numbers to a string according to get_char_from_num
def list_nums_to_str(ls):
    return "".join(list(map(lambda n: num_to_char(n), ls)))

# converts a number from 0 to 25 to a letter from 'a' to 'z'
def num_to_char(n):
    if 0 <= n <= 25:
        return chr(n + 97)
    raise ValueError("Can only convert numbers between 0 and 25.")

# converts a letter from 'a' to 'z' to a number from 0 to 25
def char_to_num(ch):
    n = ord(ch) - 97
    if 0 <= n <= 25:
        return n
    raise ValueError("Can only convert letters between 'a' and 'z'.")

#checks if the given word is all lower case and only contains letters from a to z
def lower_case_AZ(w):
    return w.islower() and w.isalpha()

#checks to see how many matches there are between the guess and the answer, regardless
#  of position, in O(n^2) time, works over lists of integers
def match_number(guess, answer):
    correct_letters = 0
    temp_answer = answer[:]
    for guess_letter in guess:
        if guess_letter in temp_answer:
            temp_answer.remove(guess_letter)
            correct_letters += 1
    return correct_letters

#z3-ified remove function - constrains a list to not have the first instance of
# the given integer, assumes that x is in ls
def remove_z3(x, ls):
    if len(ls) == 1:
        return []
    return If(ls[0] == x, ls[1:], remove_z3(x, ls[1:]))

#z3-ified match_number
def match_number_z3(guess, answer):
    correct_letters = 0
    temp_guess = guess[:]
    for answer_int in answer:
        If(num_in_list_z3(answer_int, temp_guess),
           temp_guess.remove())
    
    return correct_letters

# integrates methods and generates constraints
def main(allwords_fd, guesses_fd, sw_letters):
    allwords, guesses = get_allwords_and_guesses(allwords_fd, guesses_fd, sw_letters)

    secret_word = [ Int(f"letter_{i}") for i in range(sw_letters) ]
    
    s = Solver()

    # all of secret_word's letters must be between 'a' and 'z'
##    for letter in secret_word:
##        s.add(0 <= letter)
##        s.add(letter <= 25)

    # secret_word must be in the dictionary
    s.add(list_in_lol_z3(secret_word, allwords))

    # for each guess:
    #    matchNumber(guess, secret_word) must be the guess's given number of matches
##    for guess in guesses:
##        s.add(match_number(str_to_list_nums(guess), secret_word) == guesses[guess])

    print(s.check())
    print(s.model())
    


if __name__ == '__main__':

    main("exampleWords.txt", "example.txt", 4)

##  sw_letters = int(input("Enter the number of letters in the secret word: "))
##    main(
##        input("Enter the filename you want to load the dictionary of words from: "),
##        input("Enter the filename you want to load the history of guesses from: "),
##        sw_letters)


