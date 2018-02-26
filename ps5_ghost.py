# Problem Set 5: Ghost
# Name: 
# Collaborators: 
# Time: 
#

import random

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import string

WORDLIST_FILENAME = "ps5_words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq


# (end of helper code)
# -----------------------------------

# Actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program.

# TO DO: your code begins here!


def isValidInput(guess):
    if guess in string.ascii_letters:
        return True


def wordTest(word, wordlist):
    x = -1
    if len(word) < 3:
        return None
    else:
        if word in wordlist:
            return True
        else:
            for i in wordlist:
                if i.find(word) == 0:
                    x = i.find(word)
                    return None
            if x != 0:
                return False


def playHand():
    word = ''
    pl1 = 2
    pl2 = 1
    while len(word) < 100:
        if pl1 == 1:
            pl1 = 2
            pl2 = 1
        else:
            pl1 = 1
            pl2 = 2
        print('current word:', word)
        print('Player', pl1, '| add a letter:')
        guess = input()
        guess = guess.lower()
        
        if isValidInput(guess) != True:
            return ('cheater!')
        
        word = word + guess
        testedWord = wordTest(word, wordlist)
        
        if testedWord == True:
            print('Player', pl1, 'loses because the word', word, 'is a valid word')
            print('Player', pl2, 'wins')
            return
        if testedWord == False:
            print('Player', pl1, 'loses because no word starts with', word)
            print('Player', pl2, 'wins')
            return


def playGame():
    while True:
        cmd = input('Enter n for new game, or e to exit: ')
        if cmd == 'n':
            playHand()
            print
        elif cmd == 'e':
            break
        else:
            print("Invalid command.")


if __name__ == '__main__':
    wordlist = load_words()
    playGame()

























