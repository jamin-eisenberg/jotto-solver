from json import load
from z3 import *

import sys

# TODO: tests, README update

# In signatures, "int"s for methods with z3 in the name can mean either concrete ints or Z3Py's Int type

# a 1-string is a string of length 1, used to represent a letter

# string, string -> [string]
# takes in 2 file descriptors for the dictionary and the guesses
# generates the final constraints on the secret word and returns potential solutions
def get_possible_answers(allwords_fd, guesses_fd):
    allwords, guesses, sw_letters = get_allwords_and_guesses(allwords_fd, guesses_fd)

    secret_word = [ Int(f"letter_{i}") for i in range(sw_letters) ]
    
    s = Solver()

    # each letter in the secret_word must be between 'a' and 'z'
    for ch in secret_word:
        s.add(ch >= 0, ch <= 25)
        
    # secret_word must be in the dictionary
    s.add(list_in_lol_z3(secret_word, allwords))

    # for each guess:
    #    matching the number of guess and secret_word must be the guess's given number of matches
    next_name_count = 0
    
    for guess in guesses:
        s.add(match_number_z3(str_to_list_nums(guess), secret_word, guesses[guess]))

        next_name_count += 1

    # get all of the possible solutions for the given constraints
    answers = []

    m = get_next_model(s)
    while m is not None:       
        ans = [ -1 for i in range(sw_letters) ]

        # convert a model to a list of numbers in order of letter suffix
        for d in m.decls():
            if "letter" in d.name():
                ans[int(d.name()[7:])] = m[d].as_long()

        # add the answer converted to a string to the list
        answers.append(list_nums_to_str(ans))
        
        m = get_next_model(s)

    return answers

# [int], [int] -> Z3 Constraint
# generates a constraint for list equality between the given lists
def list_equal_z3(ls1, ls2):
    if ls1 == [] or ls2 == []:
        return ls1 == ls2
    return And(ls1[0] == ls2[0], list_equal_z3(ls1[1:], ls2[1:]))

# int, [int] -> Z3 Constraint
# generates a constraint for the given number being in the list of numbers
def num_in_list_z3(x, ls):
    if ls == []:
        return False
    return Or(ls[0] == x, num_in_list_z3(x, ls[1:]))

# [int], [[int]] -> Z3 Constraint
# generates a constraint for making x, a list of numbers, in the given list of list of numbers
def list_in_lol_z3(x, ls):
    if ls == []:
        return False
    return Or(list_equal_z3(x, ls[0]), list_in_lol_z3(x, ls[1:]))

# [int], [int] -> Z3 Constraint
# generates a constraint for making the given o equal to the number of matches between the given lists
def match_number_z3(guess, answer, o):

    def match_number_z3_acc(guess, answer, o, acc):
        if guess == []:
            return o == acc

        # if the first letter in guess is in the answer, increment the accumulator
        return If(num_in_list_z3(guess[0], answer),
                  match_number_z3_acc(guess[1:], answer, o, acc + 1),
                  match_number_z3_acc(guess[1:], answer, o, acc))

    return match_number_z3_acc(guess, answer, o, 0)

# Solver -> Model|None
# derived from https://stackoverflow.com/questions/11867611/z3py-checking-all-solutions-for-equation
# Gets the next model for a solution and applies the constraint that future solutions cannot have the same model
def get_next_model(s):
    if s.check() == sat:
        m = s.model()
        result = m
        # Create a new constraint that blocks the current model
        block = []
        for d in m:
            # create a constant from declaration
            c = d()
            block.append(c != m[d])
            
        s.add(Or(block))

        return result
    
    #if it's unsatisfiable, there are no models
    else:
        return None

# string, string -> ([[int]], {string: int}, int)
# returns a tuple with:
#   a list of list of numbers 0-25 representing words loaded from a file with the given name
#   a mapping of guesses to their match number loaded from a file with the given name
#   the assumed number of letters in the secret word
# the list of words is sorted and filtered to only include words of the given length
# the list of words is converted into a list of list of numbers 0-25
# the mapping of guesses is verified to make sure all guesses are in the dictionary
def get_allwords_and_guesses(allwords_fd, guesses_fd):

    # load in the dictionary and the guesses from files
    with open(allwords_fd) as allwords_f:
        with open(guesses_fd) as guesses_f:
            allwords = sorted(allwords_f.readlines())
            guesses = load(guesses_f)

    # assume the number of letters in secret_word
    sw_letters = len(list(guesses.keys())[0])

    # make allwords relevant by removing too long or too short words
    allwords = list(map(lambda s: s.strip(), allwords))
    allwords = list(filter(lambda s: len(s) == sw_letters and s.islower(), allwords))

    # convert the dictionary to lists of ints
    for i, s in enumerate(allwords):
        allwords[i] = str_to_list_nums(s)

    # make sure the guesses are in the dictionary
    for guess in guesses:
        if binary_search(str_to_list_nums(guess), allwords) == -1:
            raise ValueError("All guesses must be in the provided dictionary "
                             "and the same length as the secret word. "
                             f"'{guess}' violates this.")

    return allwords, guesses, sw_letters


# (X)  X, [X] -> int
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

# string -> [int]
# converts each letter in a string to a number according to get_num_from_char
def str_to_list_nums(s):
    return list(map(lambda ch: char_to_num(ch), s))

# [int] -> string
# converts a list of numbers to a string according to get_char_from_num
def list_nums_to_str(ls):
    return "".join(list(map(lambda n: num_to_char(n), ls)))

# int -> 1-string
# converts a number from 0 to 25 to a letter from 'a' to 'z'
def num_to_char(n):
    if 0 <= n <= 25:
        return chr(n + 97)
    raise ValueError("Can only convert numbers between 0 and 25.")

# 1-string -> int
# converts a letter from 'a' to 'z' to a number from 0 to 25
def char_to_num(ch):
    n = ord(ch) - 97
    if 0 <= n <= 25:
        return n
    raise ValueError("Can only convert letters between 'a' and 'z'.")




##def match_number_z3(guess, answer, o, next_name):
##    
##    def match_number_z3_acc(guess, answer, o, acc):
##        if guess == []:
##            return o == acc
##        Next = [Int(f"next{next_name}-{i}") for i in range(len(answer) - 1)]
##        return If(num_in_list_z3(guess[0], answer),
##           And(remove_z3(guess[0], answer, Next),
##               match_number_z3_acc(guess[1:], Next, o, acc + 1)),
##           match_number_z3_acc(guess[1:], answer, o, acc))
##
##    return match_number_z3_acc(guess, answer, o, 0)

##def remove_z3(x, ls, o):
##    if len(ls) <= 1:
##        return o == []
##
##    return Or(And(x == ls[0], list_equal_z3(o, ls[1:])), And(o[0] == ls[0], remove_z3(x, ls[1:], o[1:])))
    




# MAIN
if __name__ == '__main__':
    # we're recurring through at most 77,000ish words, so the limit must be raised
    sys.setrecursionlimit(10**5)

    # get the solutions for the given file descriptors
    answers = get_possible_answers("allwords_nodups.txt",
        input("Enter the filename you want to load the history of guesses from: "))

    # only give the next solution when the user presses enter
    first = True
    while answers != [] and (first or input().strip() == ""):
        first = False
        
        print(answers.pop(0))

    print("No more solutions")
            





