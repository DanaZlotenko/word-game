# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
    'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0
}

WORDLIST_FILENAME = "words.txt"


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
        freq[x] = freq.get(x, 0) + 1
    return freq



def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    word: string
    n: int >= 0
    returns: int >= 0
    """

    word_length = len(word)
    word = word.lower()
    score = 0
    value = 7 * word_length - 3 * (n - word_length)
    for i in word:
        score += SCRABBLE_LETTER_VALUES[i]
    if value > 1:
        score *= value
    else:
        return score
    return score


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    hand: dictionary (string -> int)
    """

    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=' ')  # print all on the same line
    print()  # print an empty line


def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    n: int >= 0
    returns: dictionary (string -> int)
    """

    hand = {}
    num_vowels = int(math.ceil(n / 3))

    hand['*'] = 1

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand



def update_hand(hand, word):
    """

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    new_hand = hand.copy()  # creates a new hand
    word = word.lower()

    for i in word:
        if i not in new_hand:
            break
        else:
            new_hand[i] -= 1  # deletes letter
    return new_hand



def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """

    words = []
    word = word.lower()
    lst_word = list(word)
    # checks if * is in word
    if '*' in lst_word:
        position = lst_word.index('*')
        for letter in VOWELS:
            lst_word[position] = letter
            words.append("".join(lst_word))
    else:
        words.append(word)

    # checks if possible words in word_list
    found = False
    for i in words:
        if i in word_list:
            found = True

    if not found:
        return False

    # checks if dictionary isn't empty
    word_d = get_frequency_dict(word)
    for letter, freq in word_d.items():
        if freq > hand.get(letter, 0):
            return False

    return True



def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    length = 0
    for i in hand:
        length += hand[i]
    return length


def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:


      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """

    total_score = 0
    # As long as there are still letters left in the hand:
    while calculate_handlen(hand) > 0:
        # Display the hand
        print("Current hand:", end=" ")
        display_hand(hand)
        # Ask user for input
        word = input('Enter word, or "!!" to indicate that you are finished: ')
        word = word.lower()
        # If the input is two exclamation points:
        if word == '!!':
            # End the game (break out of the loop)
            break

        # Otherwise (the input is not two exclamation points):
        else:
            # If the word is valid:
            if is_valid_word(word, hand, word_list):
                # Tell the user how many points the word earned,
                # and the updated total score
                word_score = get_word_score(word, calculate_handlen(hand))
                total_score += word_score
                print('"' + word + '"', "earned", word_score, "points. Total:", total_score, "points")

            # Otherwise (the word is not valid):
            else:
                # Reject invalid word (print a message)
                print("This is not a valid word. Please choose another word.")
            # update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, word)

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    if calculate_handlen(hand) == 0:
        print("Ran out of letters.", end=' ')
    # Return the total score as result of function
    print("Total score for this hand:", total_score, "points")
    print("--------")
    return total_score




def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """

    all_letters = VOWELS + CONSONANTS
    if letter not in hand:  # checks if letter in hand
        return hand
    while True:
        new_letter = random.choice(all_letters)  # chooses a random letter
        if new_letter in hand.keys():
            continue
        else:
            hand[new_letter] = hand[letter]  # substitutes a letter
            del hand[letter]  # deletes substituted letter
            break
    return hand


def play_game(word_list):
    """
    Allow the user to play a series of hands

    word_list: list of lowercase strings
    """
    total_hands = int(input('Enter total number of hands: '))
    final_score = 0
    letter_substituted = False
    hand_replayed = False

    for n in range(total_hands):
        hand = deal_hand(HAND_SIZE)  # deals inputed number of hands
        if not letter_substituted:
            print("Current Hand:", end=" ")
            display_hand(hand)
            substitute = input('Would you like to substitute a letter? ')  # asks if user want to substitute a letter
            if substitute.lower() == 'yes':
                letter_substituted = True
                letter = input('Which letter would you like to replace: ')
                hand = substitute_hand(hand, letter)
        hand_score = play_hand(hand, word_list)
        if not hand_replayed:  # asks if user want to replay the hand
            replay = input('Would you like to replay the hand? ')
            if replay.lower() == 'yes':
                hand_replayed = True
                new_hand_score = play_hand(hand, word_list)
                if new_hand_score > hand_score:
                    hand_score = new_hand_score
        final_score += hand_score  # calculates final score

    print("Total score over all hands:", final_score)


if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
