# /wordle.py
import collections
import getpass
from algorithm import *
import time
import random

WORD_LENGTH = 5
MAX_GUESSES = 6

def get_feedback(guess, secret_word):
    if len(guess) != len(secret_word):
        raise ValueError("Guess and secret word must have the same length.")

    feedback = [''] * len(secret_word)
    secret_counts = collections.Counter(secret_word)
    guess_counts = collections.Counter()

    # mark green
    for i in range(len(secret_word)):
        if guess[i] == secret_word[i]:
            feedback[i] = 'green'
            letter = guess[i]
            guess_counts[letter] += 1

    # mark yellow and gray
    for i in range(len(secret_word)):
        if feedback[i] == '': # ignore green
            letter = guess[i]
            # check if the letter is in secret word 
            # check for ALL occurrences found green/yellow marks.
            if letter in secret_counts and guess_counts[letter] < secret_counts[letter]:
                feedback[i] = 'yellow'
                guess_counts[letter] += 1
            else:
                feedback[i] = 'gray'

    return feedback

def display_feedback(guess, feedback):
    guess_symbols = {
        'green': '🟩',
        'yellow': '🟨',
        'gray': '⬜'
    }
    display_string = "  ".join(guess.upper())
    feedback_string = " ".join(guess_symbols[color] for color in feedback)
    print(display_string)
    print(feedback_string)
    print("---------------") # Separator line

def play_wordle():
    # print(f"You have {MAX_GUESSES} guesses to find the {WORD_LENGTH}-letter word.")

    while True:
        # show word
        #secret_word = input(f"Enter the {WORD_LENGTH}-letter secret word: ").lower()
        # hide word
        # secret_word = getpass.getpass(f"Enter the {WORD_LENGTH}-letter secret word: ").lower()

        #creates list of words from valid-guesses.txt
        secret_words = load_words_from_file('./Words/valid-guesses.txt')
        # selects random word from secret_words list
        secret_word = secret_words[random.randint(1,len(secret_words) -1)]
        if len(secret_word) == WORD_LENGTH and secret_word.isalpha():
            break
        else:
            print(f"Invalid input. Please enter exactly {WORD_LENGTH} letters.")

    # print("\n--- Game Start ---")

    guesses = 0
    # keeps track of all guesses to ensure no repeats
    prior_guesses = set()
    win = False
    history = [] 
    # dictionary for green letters {index: letter}
    green_positions = {}
    # list for yellow letters [(index, letter)]
    yellow_positions = []
    # set of yellow letters
    yellow_letters = set()
    # creates a list of all valid words from valid-guesses.txt
    valid_words = load_words_from_file('./Words/valid-guesses.txt')

    while guesses < MAX_GUESSES:
        # print(f"\nGuess {guesses + 1} of {MAX_GUESSES}")

        while True:
            #starts with first guess as 'stare'
            if guesses == 0:
                guess = 'tales'
            prior_guesses.add(guess)
            # else:
                # guess = input("Enter your guess: ").lower()
            if len(guess) == WORD_LENGTH and guess.isalpha():
                break
            else:
                print(f"Invalid guess. Please enter exactly {WORD_LENGTH} letters.")

        feedback = get_feedback(guess, secret_word)
        history.append((guess, feedback))

        # display history
        # print("\n--- History ---")
        # for g, f in history:
        #      display_feedback(g, f)

        # increment guesses
        guesses += 1

        # check for win
        if all(f == 'green' for f in feedback):
            win = True
            break
        #updates green and yellow letters' positions
        store_positions(guess, feedback, green_positions, yellow_positions,yellow_letters)
        #updates valid words
        valid_words = filter_invalid_words(valid_words, guess, feedback)
        #makes next guess based off information gathered from previous guess
        guess = make_guess(valid_words,green_positions,yellow_positions,yellow_letters)

    # game Over
    # print("\n--- Game Over ---")
    if win:
        # print(f"Congratulations! You guessed the word '{secret_word.upper()}' in {guesses} guesses!")
        return 1
    else:
        # print(f"Sorry, you ran out of guesses. The word was '{secret_word.upper()}'.")
        return 0

if __name__ == "__main__":
    wins = 0
    for i in range(1000):
        game = play_wordle()
        if game:
            wins+=1
    print(f'Won {wins} / 1000')
        
    