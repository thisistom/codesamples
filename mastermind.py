#!/usr/bin/env python
"""
Mastermind - a simple command-line logic game.

The game will pick a numerical code, and the player must guess the code in as
few tries as possible. The game will tell users how many correct digits they
have, but not which ones are correct. Users can optionally specify the
difficulty of the game using command line arguments.

Usage: mastermind.py [numberOfDigits [maximumDigitSize (2-9)]]

e.g. "mastermind.py 3 4" will create 3 digit code made up of digits from 1-4.

Challenge taken from http://usingpython.com/python-programming-challenges.
"""

import sys
import random
import readline # makes raw_input() friendlier


class Mastermind(object):
    """
    A class representing a game of mastermind. Chooses a combination of numbers
    on initialisation, and validates guesses (returning the number of digits in
    the guess which are correct) against that code until C{reset()} is called.
    """

    # Class Variables ---------------------------------------------------------

    # Variables defining difficulty - the number of random numbers to guess,
    # and the maximum digit that will be chosen.
    DefaultCount = 4
    DefaultMaxDigit = 4

    # Public Instance Functions -----------------------------------------------

    def __init__(self, count=DefaultCount, maxDigit=DefaultMaxDigit):
        """
        Initializes an instance of the class with the given settings.

        @type count: C{int}
        @type maxDigit: C{int}
        @param count: The number of digits to use in the game (optional).
        @param maxDigit: The maximum size of the digit to use in the game
            (optional).
        """
        self.reset(count, maxDigit)

    def reset(self, count=DefaultCount, maxDigit=DefaultMaxDigit):
        """
        Resets the game using the given settings.

        @type count: C{int}
        @type maxDigit: C{int}
        @param count: The number of digits to use in the game (optional).
        @param maxDigit: The maximum size of the digit to use in the game
            (optional).
        """
        self.__count = count
        self.__maxDigit = maxDigit
        self.__numGuesses = 0

        # Seed the random number generator based on the current system time
        random.seed()

        # Create a new code
        self.__code = self.__generateNewCode()

    def checkGuess(self, guess):
        """
        Checks the given guess against the current code.

        @type guess: C{str}
        @rtype: C{int}
        @param guess: The guess to validate against the current code.
        @return: The number of digits in the given guess which match the
            current code, or -1 if the guess was invalid.
        """
        # Split the guess into a list of integers
        guessInts = self.__splitGuess(guess)
        if len(guessInts) != self.__count:
            # Exit early if there are the wrong number of elements
            return -1

        # Be kind - only count this as a guess if it's valid
        self.__numGuesses += 1

        # Now check the guess - return the number of digits that match
        return sum(1 for (x, y) in zip(guessInts, self.__code) if x == y)

    def getMaxDigit(self):
        """
        @rtype: C{int}
        @return: The maximum digit which will be used in this game.
        """
        return self.__maxDigit

    def getCount(self):
        """
        @rtype: C{int}
        @return: The number of digits that will be used in this game.
        """
        return self.__count

    def getNumGuesses(self):
        """
        @rtype: C{int}
        @return: The number of guesses that the user has made in this game.
        """
        return self.__numGuesses

    # Private Instance Functions ----------------------------------------------

    def __generateNewCode(self):
        """
        @rtype: C{list} of C{int}
        @return: A new set of random numbers according to the current values of
            self.__maxSize and self.__count. Numbers will be between 1 and
            self.__maxSize inclusive.
        """
        return [1 + int(random.random() * self.__maxDigit)
                for x in xrange(self.__count)]

    def __splitGuess(self, guess):
        """
        Splits the given string representing a guess by the user into a list of
        integers. We permit either a single string of digits (e.g. "1234") or
        space-separated digits (e.g. "1 2 3 4").

        @type guess: C{str}
        @rtype: C{list} of C{int}
        @param guess: The guess to split into a list of integers.
        @return: A list of integers split from the given guess, if any could be
            extracted.
         """
        strippedGuess = guess.strip()
        if " " in strippedGuess:
            # There are spaces - split into individual digits
            splitGuess = strippedGuess.split()
        else:
            # No spaces - assume this is a single string of digits
            splitGuess = list(guess)

        # Convert all elements to integers and return those which are in the
        # correct range
        return [int(x) for x in splitGuess
                if x.isdigit() and 0 < int(x) <= self.__maxDigit]


# Protected Module Functions --------------------------------------------------

def _isQuit(guess):
    """
    @type guess: C{str}
    @rtype: C{bool}
    @param guess: The string to evaluate whether the user wants to quit.
    @return: C{True} if the given input means that the user wants to quit,
        otherwise C{False}.
    """
    lowerCaseGuess = guess.lower()
    return (lowerCaseGuess.startswith("quit")
            or lowerCaseGuess.startswith("exit"))

def _printUsageAndExit(message=""):
    """
    Prints the correct usage of this script and exits.

    @type message: C{str}
    @param message: An optional message to print before printing the usage.
    """
    print("%s\nUsage : %s [numberOfDigits [maximumDigitSize (2-9)]]"
          % (message, __file__))
    exit(2)

def _getInput(prompt):
    """
    Displays the given prompt, and waits for input from the user.

    @type prompt: C{str}
    @rtype: C{str}
    @param prompt: The prompt to display when requesting data from the user.
    @return: The input received from the user.
    """
    return raw_input(prompt)

# Public Module Functions -----------------------------------------------------

def play(count=Mastermind.DefaultCount, maxDigit=Mastermind.DefaultMaxDigit):
    """
    The main game function. Creates a Mastermind instance with the given
    settings, and passes user input into it until the user correctly guesses
    the code, then resets the game again. Continues until the user types "quit"
    or "exit".

    @type count: C{int}
    @type maxDigit: C{int}
    @param count: The number of digits to use in the game (optional).
    @param maxDigit: The maximum size of the digit to use in the game
        (optional).
    """
    # Store how many possible combinations there are
    numCombinations = pow(maxDigit, count)

    # Create the main game object
    game = Mastermind(count, maxDigit)

    # Print some welcome text
    welcomeText = ("\n --- Let's play MASTERMIND! ---\n"
                   "Guess the code: %d digits between 1 and %d"
                   % (count, maxDigit))
    print(welcomeText)

    # Loop until the user asks to quit
    while True:
        prompt = " %d > " % (game.getNumGuesses() + 1)
        guess = _getInput(prompt)

        if _isQuit(guess):
            # Let the user quit
            print ("Thanks for playing!")
            break

        if not len(guess.strip()):
            # No input - try again
            continue

        numCorrect = game.checkGuess(guess)
        if numCorrect < 0:
            # The guess wasn't valid
            print ("Please enter %d digits between 1 and %d"
                   % (count, maxDigit))
            continue

        # Print some asterisks to show how many digits they have correct
        print ("%s[%s%s]" % ((" " * (len(prompt) - 1), ("*" * numCorrect),
                             ("-" * (count - numCorrect)))))

        if numCorrect == count:
            # They won! Reset the game and go again.
            print ("Well done! That took you %d attempts, out of %d possible "
                   "combinations." % (game.getNumGuesses(), numCombinations))
            game.reset(count, maxDigit)
            print(welcomeText)


if __name__ == "__main__":
    # Get default values for the game difficulty
    count = Mastermind.DefaultCount
    maxDigit = Mastermind.DefaultMaxDigit

    # Validate any command line arguments.
    args = sys.argv[1:]
    if args:
        if len(args) > 2:
            # Wrong number of args
            _printUsageAndExit("Wrong number of arguments.")
        if any((not x.isdigit() for x in args)):
            # Args aren't digits
            _printUsageAndExit("Arguments must be digits.")

        count = int(args[0])
        if len(args) > 1:
            maxDigit = int(args[1])
            if not 1 < maxDigit <= 9:
                # Max digit arg is out of range
                _printUsageAndExit("Maximum digit argument out of range: %d."
                                   % maxDigit)

    # Play the game
    play(count, maxDigit)
