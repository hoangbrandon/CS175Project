# /wordle.py
import collections
import getpass

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
    print(f"You have {MAX_GUESSES} guesses to find the {WORD_LENGTH}-letter word.")

    while True:
        # show word
        #secret_word = input(f"Enter the {WORD_LENGTH}-letter secret word: ").lower()
        # hide word
        secret_word = getpass.getpass(f"Enter the {WORD_LENGTH}-letter secret word: ").lower()
        if len(secret_word) == WORD_LENGTH and secret_word.isalpha():
            break
        else:
            print(f"Invalid input. Please enter exactly {WORD_LENGTH} letters.")

    print("\n--- Game Start ---")

    guesses = 0
    win = False
    history = [] 

    while guesses < MAX_GUESSES:
        print(f"\nGuess {guesses + 1} of {MAX_GUESSES}")

        while True:
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

    # game Over
    print("\n--- Game Over ---")
    if win:
        print(f"Congratulations! You guessed the word '{secret_word.upper()}' in {guesses} guesses!")
    else:
        print(f"Sorry, you ran out of guesses. The word was '{secret_word.upper()}'.")

if __name__ == "__main__":
    play_wordle()
