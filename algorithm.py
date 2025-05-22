""" Creates a list of words from a .txt file. """
def load_words_from_file(filepath):
    with open(filepath, 'r') as file:
        words = [line.strip().lower() for line in file]
    return words

""" Removes words with detected grey letters and words without correct green letters. """
def filter_invalid_words(valid_words, guess, feedback, prior_guesses):
    incorrect_letters = set()
    valid_letters = set()
    green_positions = {}

    for i, color in enumerate(feedback):
        letter = guess[i]
        if color == 'green':
            green_positions[i] = letter
            valid_letters.add(letter)
        elif color == 'yellow':
            valid_letters.add(letter)
        elif color == 'gray':
            incorrect_letters.add(letter)
    truly_incorrect = incorrect_letters - valid_letters

    filtered = []
    for word in valid_words:
        if any(letter in word for letter in truly_incorrect):
            continue
        if any(word[i] != letter for i, letter in green_positions.items()):
            continue
        if word in prior_guesses:
            continue
        filtered.append(word)
    return filtered

""" Adds to green and yellow positions from feedback of a new guess. """
def store_positions(guess,guess_feedback,green_positions, yellow_positions, yellow_letters):
    for i, color in enumerate(guess_feedback):
        if color == 'green':
            green_positions[i] = guess[i]
        elif color == 'yellow':
            yellow_positions.append((i, guess[i]))
            yellow_letters.add(guess[i])

""" Gives a word a score based on the amount of correct green letters and yellow letters. """
def score_word(word, green_positions, yellow_positions, yellow_letters):
    score = 0
    for i, letter in enumerate(word):
        if i in green_positions and word[i] == green_positions[i]:
            score += 2
        elif letter in yellow_letters and all((i != yp[0] or letter != yp[1]) for yp in yellow_positions):
            score += 1
    return score

""" Scores all valid words and selects the word with the highest score. """
def make_guess(valid_words,green_positions, yellow_positions,yellow_letters):
    scored = []
    for word in valid_words:
        scored.append((word, score_word(word, green_positions, yellow_positions,yellow_letters)))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[0][0]
