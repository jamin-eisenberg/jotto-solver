from json import load
import collections
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


def match_number_z3(guess, answer, o):
    
    def match_number_z3_acc(guess, answer, o, acc):
        if guess == []:
            return o == acc
        Next = [Int(f"x{i}") for i in range(len(answer) - 1)]
        return If(num_in_list_z3(guess[0], answer),
           And(remove_z3(guess[0], answer, Next),
               match_number_z3_acc(guess[1:], Next, o, acc + 1)),
           match_number_z3_acc(guess[1:], answer, o, acc))

    return match_number_z3_acc(guess, answer, o, 0)

  
##def remove(x, Ls):
####    if simplify(Ls) == nil:
####        return nil
##
##    if x == simplify(car(Ls)):
##        return cdr(Ls)
##    else:
##        return cons(car(Ls), remove(x, cdr(Ls)))

##def remove_z3(x, Ls, o):
##    if Ls == []:
##        return o == []
##    
##    return If(x == simplify(car(Ls)), o == cdr(Ls), o == cons(car(Ls), remove_z3(x, cdr(Ls))))

def remove_z3(x, Ls, o):
    if o == []:
        return o == []
    if len(Ls) <= 1:
        return o == []
    
    return If(x == Ls[0], list_equal_z3(o, Ls[1:]),
              And(o[0] == Ls[0], remove_z3(x, Ls[1:], o[1:])))


#z3-ified remove function - constrains a list to not have the first instance of
# the given integer, assumes that x is in ls
##def remove_z3(x, Ls):
##    if Ls == cons(x, nil):
##        return nil
##    return If(simplify(simplify(car(Ls)) == x), simplify(cdr(Ls)),
##              cons(simplify(car(Ls)).as_long(), remove_z3(x, simplify(cdr(Ls)))))
##
## 
##
##def remove_z3_v2(x, Ls):
##    return If(simplify(car(Ls)).as_long() == x, simplify(cdr(Ls)),
##              cons(car(Ls), remove_z3(x, simplify(cdr(Ls)))))
##
## 
##
##
###z3-ified match_number
##def match_number_z3(guess, answer):
##    correct_letters = 0
##    temp_guess = guess[:]
##    for answer_int in answer:
##        If(num_in_list_z3(answer_int, temp_guess),
##           temp_guess.remove())
##    
##    return correct_letters






def get_next_model(s):
    if s.check() == sat:
        m = s.model()
        result = m
        # Create a new constraint the blocks the current model
        block = []
        for d in m:
            # d is a declaration
            if d.arity() > 0:
                raise Z3Exception("uninterpreted functions are not supported")
            # create a constant from declaration
            c = d()
            if is_array(c) or c.sort().kind() == Z3_UNINTERPRETED_SORT:
                raise Z3Exception("arrays and uninterpreted sorts are not supported")
            block.append(c != m[d])
        s.add(Or(block))

        return result
    
    else:
        print("No more solutions")






# integrates methods and generates constraints
def main(allwords_fd, guesses_fd, sw_letters):
    allwords, guesses = get_allwords_and_guesses(allwords_fd, guesses_fd, sw_letters)

    secret_word = [ Int(f"letter_{i}") for i in range(sw_letters) ]
    
    s = Solver()

    for ch in secret_word:
        s.add(ch >= 0, ch <= 25)
        
    # secret_word must be in the dictionary
    s.add(list_in_lol_z3(secret_word, allwords))

    # for each guess:
    #    matchNumber(guess, secret_word) must be the guess's given number of matches
    
    for guess in guesses:

##    guess = "have"
        if guess != "sows":
            continue
        print(str_to_list_nums(guess), secret_word, guesses[guess])
        s.add(match_number_z3(str_to_list_nums(guess), secret_word, guesses[guess]))
        if guess == "sows":
            break

##    for m in get_models(s.assertions(), 5):

##    print(s.check())
##
##    m = s.model()
##
    first = True

    while first or input().strip() == "":
        first = False
        
        m = get_next_model(s)
            
        ans = [ -1 for i in range(sw_letters) ]

        for d in m.decls():
            if "letter" in d.name():
                ans[int(d.name()[7:])] = m[d].as_long()

        print(list_nums_to_str(ans))

    


if __name__ == '__main__':

    main("allwords.txt", "example.txt", 4)


##    print(simplify(If(car(cons(1, nil)) == 1, cons(2, nil), cons(3, nil))))
    

##  sw_letters = int(input("Enter the number of letters in the secret word: "))
##    main(
##        input("Enter the filename you want to load the dictionary of words from: "),
##        input("Enter the filename you want to load the history of guesses from: "),
##        sw_letters)


