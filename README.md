# CS2800Final
SMT solver for Jotto

For our project, we'd like to write a Java program to convert a game state of Jotto into a boolean 
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
example, given the history from lines 183 - 188, the program would return true if "dogs" was in the list
(or if "pwnk" was in the list - because that would give all of the same results). The meat of programming
we'll do will be converting the guess history (and our word list) into a boolean satisfiability problem.
The results of that would just be plugged into a SAT solver.

Our initial searches revealed no SAT solving of this game. Algorithms have been developed to make optimal
guesses, but as far as we could tell, no one has done what we are trying to do.

We think this project is in scope for this course because it actually feels like it has a lot to do 
with constraint programming. "My word must share exactly three letters with the one you just said,"
seems like a strong indication of that. Additionally, what this (ideally) boils down to is a boolean
satisfiability problem, which seems part of the core of what we've been studying.
