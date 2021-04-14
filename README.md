# CS2800Final
SMT Constraint Generator for Jotto

For our project, we'd like to write a Python program to convert a game state of Jotto into a boolean 
satisfiability problem, the solution of which will tell us whether there is a word that fits the 
restrictions imposed by previous guesses.

First, it's important to understand the game of Jotto. As a reference, it's fairly similar to
mastermind, but with words. When played with humans, there is a guesser and a word-holder. The
word-holder discloses the length of their word to the guesser. The guesser then guesses a series
of English words of the given length. The word-holder responds to each guess with a number corresponding
to how many letters the guessed word has in common with their word. For example:

Word-holder: 4 (thinking of "dogs")  
Guesser: have  
Word-holder: 0  
Guesser: slip  
Word-holder: 1  
Guesser: coup  
Word-holder: 1  
Guesser: sows  
Word-holder: 2 (one of the "s"s lines up with the "s" in "dogs", and the "o" lines up)  
Guesser: suds  
Word-holder: 2  
Guesser: dost  
Word-holder: 3  
Guesser: rods  
Word-holder: 3  
Guesser: dons  
Word-holder: 3  
Guesser: dogs  
Word-holder: You got it. Good job, friend!  

Given a guess history like a subset of the example above, the end result of our program will be a boolean
that represents whether our word list contains a word that "passes" all of the parts of the history. For
example, given the history above, the program would return true if "dogs" was in the list
(or if "pwnk" was in the list - because that would give all of the same results). The meat of programming
we'll do will be converting the guess history (and our word list) into a boolean satisfiability problem.
The results of that would just be plugged into a SAT solver.

Our initial searches revealed no SAT solving of this game. Algorithms have been developed to make optimal
guesses, but as far as we could tell, no one has done what we are trying to do.

We think this project is in scope for this course because it actually feels like it has a lot to do 
with constraint programming. "My word must share exactly three letters with the one you just said,"
seems like a strong indication of that. Additionally, what this (ideally) boils down to is a boolean
satisfiability problem, which seems part of the core of what we've been studying.

# Use Instructions
(Note that these isntrcutions are for the finished product, which this is not, yet.)

In order to use this project, you will need Z3Py, an SMT solver for Python. This can be installed using pip. More detailed instructions can be found here: https://github.com/Z3Prover/z3  

Once Z3Py is installed, you should be able to run main.py. Before you do that, though, you may want to generate some guesses with guess_generator.py. Its use is simple. It will ask you to enter the words that were guesses, then the corresponding number that the word-holder said. When you are done, use "s" to save the information you entered to a text file that is readable by main.py.  

When you're ready, you can run main.py. It will prompt you to enter a path to the dictionary you'd like to use. You can create your own custom dictionary, or use allwords.txt, which contains tens of thousands of English words. After you've selected a dictionary, it will prompt you to enter a location to find your guesses. Enter the location you saved the guesses to when using the guesses_generator.

When you've entered this, the program should give you a list of words that satisfy the guesses you've provided according to the rules of the game. If not, it likely says that the guesses you've provided are unsatisfiable. This means that the word-holder picked a word that is not in the dictionary or they made a mistake in assigning numbers to guesses.

