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

def test_wordle():
    # print(f"You have {MAX_GUESSES} guesses to find the {WORD_LENGTH}-letter word.")

    while True:
        # show word
        # secret_word = input(f"Enter the {WORD_LENGTH}-letter secret word: ").lower()
        # hide word
        # secret_word = getpass.getpass(f"Enter the {WORD_LENGTH}-letter secret word: ").lower()

        #creates list of words from valid-guesses.txt
        secret_words = load_words_from_file('./Words/shuffled_real_wordles.txt')
        # selects random word from secret_words list
        secret_word = secret_words[random.randint(1,len(secret_words) -1)]
        if len(secret_word) == WORD_LENGTH and secret_word.isalpha():
            break
        else:
            print(f"Invalid input. Please enter exactly {WORD_LENGTH} letters.")

    # print("\n--- Game Start ---")

    guesses = 0
    win = False
    history = [] 

    all_allowed_guesses = load_words_from_file('./Words/valid-guesses.txt')
    actual_possible_answers = load_words_from_file('./Words/shuffled_real_wordles.txt')
    potential_solutions = set(actual_possible_answers) # Start with actual Wordles as candidates

    while guesses < MAX_GUESSES:
        # print(f"\nGuess {guesses + 1} of {MAX_GUESSES}")

        while True:
            #starts with first guess as 'stare'
            if guesses == 0:
                guess = 'slate'
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
        #updates valid words
        #makes next guess based off information gathered from previous guess
        prev = guess
        guess, potential_solutions = make_next_guess(prev, feedback, potential_solutions, all_allowed_guesses)

    # game Over
    # print("\n--- Game Over ---")
    if win:
        print(f"Congratulations! You guessed the word '{secret_word.upper()}' in {guesses} guesses!")
        return 1
    else:
        print(f"Sorry, you ran out of guesses. The word was '{secret_word.upper()}'.")
        return 0
    

def play_wordle(r):
    # print(f"You have {MAX_GUESSES} guesses to find the {WORD_LENGTH}-letter word.")
        

    if r:
        while True:
            #creates list of words from valid-guesses.txt
            secret_words = load_words_from_file('./Words/shuffled_real_wordles.txt')
            # selects random word from secret_words list
            secret_word = secret_words[random.randint(1,len(secret_words) -1)]

            if len(secret_word) == WORD_LENGTH and secret_word.isalpha():
                break
            else:
                print(f"Invalid input. Please enter exactly {WORD_LENGTH} letters.")
    else:
        while True:
            # show word
            secret_word = input(f"Enter the {WORD_LENGTH}-letter secret word: ").lower()
            # hide word
            # secret_word = getpass.getpass(f"Enter the {WORD_LENGTH}-letter secret word: ").lower()

            if len(secret_word) == WORD_LENGTH and secret_word.isalpha():
                break
            else:
                print(f"Invalid input. Please enter exactly {WORD_LENGTH} letters.")

    # print("\n--- Game Start ---")

    guesses = 0
    win = False
    history = [] 

    all_allowed_guesses = load_words_from_file('./Words/valid-guesses.txt')
    actual_possible_answers = load_words_from_file('./Words/shuffled_real_wordles.txt')
    potential_solutions = set(actual_possible_answers) # Start with actual Wordles as candidates

    while guesses < MAX_GUESSES:
        # print(f"\nGuess {guesses + 1} of {MAX_GUESSES}")

        while True:
            # guess = input("Enter your guess: ").lower()
            if guesses > 0:
                use_bot = input("Do you want the bot to suggest your next guess? (y/n): ").strip().lower() == 'y'
                if use_bot:
                    guess, potential_solutions = make_next_guess(prev, feedback, potential_solutions, all_allowed_guesses)
                    print(f"[BOT SUGGESTS] Try: {guess.upper()}")
                    user_input = input("Press [Enter] to accept or type your own guess: ").strip().lower()
                    if user_input:
                        guess = user_input
            else:
                guess = input("Enter your guess: ").lower()

            if len(guess) == WORD_LENGTH and guess.isalpha():
                break
            else:
                print(f"Invalid guess. Please enter exactly {WORD_LENGTH} letters.")

        feedback = get_feedback(guess, secret_word)
        history.append((guess, feedback))

        # display history
        print("\n--- History ---")
        for g, f in history:
             display_feedback(g, f)

        # increment guesses
        guesses += 1

        # check for win
        if all(f == 'green' for f in feedback):
            win = True
            break
        #updates valid words
        #makes next guess based off information gathered from previous guess
        prev = guess
        # update potential
        _, potential_solutions = make_next_guess(prev, feedback, potential_solutions, all_allowed_guesses)

    # game Over
    # print("\n--- Game Over ---")
    if win:
        print(f"Congratulations! You guessed the word '{secret_word.upper()}' in {guesses} guesses!")
        return 1
    else:
        print(f"Sorry, you ran out of guesses. The word was '{secret_word.upper()}'.")
        return 0
    

def testing_bot():
    wins = 0
    games = int(input("How many games to simulate?: "))
    for i in range(games):
        game = test_wordle()
        if game:
            wins+=1
    print(f'Won {wins} / {games}')

if __name__ == "__main__":
    choice = input(
        "\n--- Wordle Game Menu ---\n"
        "T - Test wordle bot x times \n"
        "P - Play a random Wordle\n"
        "F - Let a friend play your Wordle (you set the word)\n"
        "Q - Quit\n\n"
        "What mode would you like to play?: "
    ).strip().lower()

    if choice == "t":
        testing_bot()
    elif choice == "p":
        play_wordle(True)
    elif choice == "f":
        play_wordle(False)

        
    