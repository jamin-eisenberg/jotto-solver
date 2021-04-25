from json import load
from z3 import *

import sys

# we're recurring through at most 77,000ish words
sys.setrecursionlimit(10**5)

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
    ls_copy = ls[:]
    if ls_copy == []:
        return False
    return Or(ls_copy[0] == x, num_in_list_z3(x, ls_copy[1:]))

# generates a constraint for list equality between the given lists
def list_equal_z3(ls1, ls2):
    if ls1 == [] or ls2 == []:
        return ls1 == ls2
    return And(ls1[0] == ls2[0], list_equal_z3(ls1[1:], ls2[1:]))

# generates a constraint for making x, a Python list of numbers, in a Python list of list of numbers
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
    allwords = list(filter(lambda s: len(s) == sw_letters and s.islower(), allwords))

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

def match_number(guess, answer):

    def match_number_acc(guess, answer, acc):
        if guess == []:
            return acc

        if guess[0] in answer:                
            Next = answer[:]
            Next.remove(guess[0])
            return match_number_acc(guess[1:], Next, acc + 1)
        else:
            return match_number_acc(guess[1:], answer, acc)

    return match_number_acc(guess, answer, 0)


def match_number_z3(guess, answer, o, next_name):
    
    def match_number_z3_acc(guess, answer, o, acc):
        if guess == []:
            return o == acc
        Next = [Int(f"next{next_name}-{i}") for i in range(len(answer) - 1)]
        return If(num_in_list_z3(guess[0], answer),
           And(remove_z3(guess[0], answer, Next),
               match_number_z3_acc(guess[1:], Next, o, acc + 1)),
           match_number_z3_acc(guess[1:], answer, o, acc))

    return match_number_z3_acc(guess, answer, o, 0)

def remove_z3(x, Ls, o):
    if len(Ls) <= 1:
        return o == []
    
    return If(x == Ls[0], Or(list_equal_z3(o, Ls[1:]), And(o[0] == Ls[0], remove_z3(x, Ls[1:], o[1:]))),
              And(o[0] == Ls[0], remove_z3(x, Ls[1:], o[1:])))

def get_next_model(s):
    if s.check() == sat:
        m = s.model()
        result = m
        # Create a new constraint the blocks the current model
        block = []
        for d in m:
            # create a constant from declaration
            c = d()
            block.append(c != m[d])
            
        s.add(Or(block))

        return result
    
    else:
        return None

# integrates methods and generates constraints
def main(allwords_fd, guesses_fd, sw_letters):
    allwords, guesses = get_allwords_and_guesses(allwords_fd, guesses_fd, sw_letters)

    secret_word = [ Int(f"letter_{i}") for i in range(sw_letters) ]
    
    s = Solver()

    # each letter in the secret_word must be between 'a' and 'z'
    for ch in secret_word:
        s.add(ch >= 0, ch <= 25)
        
    # secret_word must be in the dictionary
    s.add(list_in_lol_z3(secret_word, allwords))

    # for each guess:
    #    matchNumber(guess, secret_word) must be the guess's given number of matches
    next_name_count = 0
    
    for guess in guesses:
        s.add(match_number_z3(str_to_list_nums(guess), secret_word, guesses[guess], str(next_name_count)))

        next_name_count += 1

    answers = set(())


    m = get_next_model(s)
    while m is not None:
        ans = [ -1 for i in range(sw_letters) ]

        for d in m.decls():
            if "letter" in d.name():
                ans[int(d.name()[7:])] = m[d].as_long()

        answers.add(list_nums_to_str(ans))
        
        m = get_next_model(s)

    answers = list(answers)

    first = True

    while answers != [] and (first or input().strip() == ""):
        first = False
        
        print(answers.pop(0))

    print("No more solutions")

    


if __name__ == '__main__':
    main("allwords.txt", "examples3.txt", 3)

##  sw_letters = int(input("Enter the number of letters in the secret word: "))
##    main(
##        input("Enter the filename you want to load the dictionary of words from: "),
##        input("Enter the filename you want to load the history of guesses from: "),
##        sw_letters)


