# Problem Set 5: 6.00 Word Game
# Name: 
# Collaborators: 
# Time: 
#

import random
import string
import time
import itertools

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "ps5_words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print ("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print ("  ", len(wordlist), "words loaded.")
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


#
# Problem #1: Scoring a word
#
def get_word_score(word, n, time):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    The score for a word is the sum of the points for letters
    in the word, plus 50 points if all n letters are used on
    the first go.

    Letters are scored as in Scrabble; A is worth 1, B is
    worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string (lowercase letters)
    returns: int >= 0
    """
    # TO DO ...
    x = 0
    word = word.lower()
    for i in word:
        x += SCRABBLE_LETTER_VALUES.get(i)
    if time < 1:
        time = 1
    x = x / time
    if len(word) >= 7:
        x += 50
    return x


def get_words_to_points(word_list):
    result = {}
    for i in word_list:
        result.update({i:int(get_word_score(i, len(i), 0))})
    return result


#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end = " ")              # print all on the same line
    print                              # print an empty line

#
# Make sure you understand how this function works and what it does!
#

def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """ 
    hand={}
    num_vowels = int(n / 2)  #-----------------------------------------------------------------<<
    
    for i in range(num_vowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(num_vowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
    return hand


#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not mutate hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    # TO DO ...
    result = hand
    for i in word:
        if result[i] == 1:
            del result[i]
        else:
            result[i] = result[i]-1
    return result


#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, points_dict):
    wordDict = {}
    for x in word:
        wordDict[x] = wordDict.get(x,0) + 1

    if word not in points_dict:
        return False
    
    for i in wordDict:
        if i not in hand:
            return False
        elif wordDict[i] > hand[i]:
                return False
    return True


##def is_valid_word(word, hand, points_dict):
##    start = time.time()
##    for letter in word:
##        if freq[letter] > hand.get(letter, 0):
##            return False
##    return word in points_dict



##def is_valid_word(word, hand, word_list):
##    if word not in word_list:
##        return False 
##
##    wordDict = {}
##    for x in word:
##        wordDict[x] = wordDict.get(x,0) + 1
##    for i in wordDict:
##        if i not in hand:
##            return False
##        elif wordDict[i] > hand[i]:
##                return False
##    return True


#
# Problem #4: Playing a hand
#


def timeLimit(timeLimitUser, elapsedTime, totTime):
    if timeLimitUser < (elapsedTime + totTime):
        return True
    else:
        return False


def get_time_limit(points_dict, k):
    start_time = time.time()
    for word in points_dict:
        get_frequency_dict(word)
        get_word_score(word, HAND_SIZE, 0)
    end_time = time.time()
    return (end_time - start_time) * k


##Couldn't do the "easier" / simpler word guesser, moving on to the faster one.

##def pick_best_word(hand, points_dict):
##    """
##    hand = dict
##    points_dict = dict
##    """
##    guess = ''
##    guessTemp = ''
##    newHand = ''
##    for letter in hand.keys():
##        for j in range(hand[letter]):
##            newHand += letter
##            
##    for i in range(1, 7):
##        for letter in newHand:
##            while len(guess) <= i:
##
##        if guessTemp in points_dict:
##            if points_dict[guessTemp] > points_dict[guess]:
##                guess = points_dict[guessTemp]


def get_word_rearrangements(word_list):
    rearrange_dict = {}
    for i in word_list:
        rearrange_dict[''.join(sorted(i))] = i
    return rearrange_dict


def pick_best_word_faster(hand, rearrange_dict, points_dict, playerTimeLimit):
    #start = time.time()                                        tested, good results
    #elapsedTime = 0                                            tested, good results

    handSet = []
    for letter in hand.keys():
        for j in range(hand[letter]):
            handSet.append(letter)
    handSet = ''.join(handSet)
    
    bestGuess = 'aa'
    #while elapsedTime < playerTimeLimit:                       tested, good results
    for m in range(2, len(handSet)+1):
        handComb = list(itertools.combinations(handSet, m))
        for i in handComb:
            guess = ''.join(sorted(i))
            if guess in rearrange_dict:
                if points_dict[rearrange_dict[guess]] > points_dict[bestGuess]:
                    bestGuess = rearrange_dict[guess]
    #elapsedTime = time.time() - start                          tested, good results
    if bestGuess == 'aa':
        bestGuess = '.'
    return bestGuess


def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * When a valid word is entered, it uses up letters from the hand.

    * After every valid word: the score for that word and the total
      score so far are displayed, the remaining letters in the hand 
      are displayed, and the user is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing a single
      period (the string '.') instead of a word.

    * The final score is displayed.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
    """
    # TO DO ...

    timeLimitUser = playerTimeLimit
    totTime = 0
    score = 0
    
    while sum(hand.values()) > 1:
        print('make a word using these letters: ')
        display_hand(hand)
        print()
        start = time.time()
        guess = pick_best_word_faster(hand, rearrange_dict, points_dict, playerTimeLimit)
        print(guess)
        elapsedTime = (time.time() - start)
        totTime += elapsedTime
        
        if guess == '.':
            print('end of hand, your score is:', score)
            return score

        if totTime > timeLimitUser:
            print(('out of time, your score is %0.2f')%(score))
            return score
        
        if is_valid_word(guess, hand, word_list) == False:
            print(guess, 'is not a valid word, try again')
        else:
            wordScore = get_word_score(guess, len(guess), elapsedTime)
            print('you scored', wordScore, 'points for this word')
            score = score + wordScore
            hand = update_hand(hand, guess)
        
        print('your total score is: ', score)
        print(('your guess took: %0.2f sec')%(elapsedTime))
        print(('time remaining: %0.2f')%(timeLimitUser - totTime))
        print()
    return score




#
# Problem #5: Playing a game
# Make sure you understand how this code works!
# 
def play_game(word_list):
    """
    Allow the user to play an arbitrary number of hands.

    * Asks the user to input 'n' or 'r' or 'e'.

    * If the user inputs 'n', let the user play a new (random) hand.
      When done playing the hand, ask the 'n' or 'e' question again.

    * If the user inputs 'r', let the user play the last hand again.

    * If the user inputs 'e', exit the game.

    * If the user inputs anything else, ask them again.
    """
    # TO DO ...
##    print ("play_game not implemented.")         # delete this once you've completed Problem #4
##    play_hand(deal_hand(HAND_SIZE), word_list) # delete this once you've completed Problem #4
    
    ## uncomment the following block of code once you've completed Problem #4
    hand = deal_hand(HAND_SIZE) # random init
    while True:
        cmd = input('Enter n to deal a new hand, r to replay the last hand, or e to end game: ')
        if cmd == 'n':
            hand = deal_hand(HAND_SIZE)
            play_hand(hand.copy(), word_list)
            print
        elif cmd == 'r':
            play_hand(hand.copy(), word_list)
            print
        elif cmd == 'e':
            break
        else:
            print("Invalid command.")

#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    points_dict = get_words_to_points(word_list)
    rearrange_dict = get_word_rearrangements(word_list)
    playerTimeLimit = get_time_limit(points_dict, 10)
    play_game(word_list)



##    Problem 5
    
##    pick_best_word not implemented
    
##    pick_best_word_faster
##    ---------------------
##    n = number of possible letter combinations in hand [with itertools.combinations] = O(n)
##    validating if guess is in rearrange_dict = O(n)*O(1)
##    m = viable guesses, check for point count and compare with bestGuess = O(m)*O(1)
##
##    O(n) + O(n)*O(1) + O(m)*O(1)
##
##    O(2n) + O(m)
##
##    if word list grows, time complexity for validation doesn't change,
##    but time for getting rearrange_dict and points_dict increase linearly
##    if size of hand grows, time complexity increases linearly for each additional letter








    
