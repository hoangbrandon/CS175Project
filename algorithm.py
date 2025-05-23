""" Creates a list of words from a .txt file. """


def load_words_from_file(filepath):
    with open(filepath, 'r') as file:
        words = [line.strip().lower() for line in file]
    return words

""" Removes words with detected grey letters and words without correct green letters. """
def filter_invalid_words(valid_words, guess, feedback):
    guess = guess.lower()

    grey_positions = {}
    yellow_positions = {}
    green_positions = {}

    current_yellow = {}

    valid_letters = set() # green/yellow
    invalid_letters = set() # grey

    for i, color in enumerate(feedback):
        letter = guess[i]
        if color == 'green':
            green_positions[i] = letter
            valid_letters.add(letter)
        elif color == 'yellow':
            yellow_positions[i] = letter
            if letter in current_yellow:
                current_yellow[letter] += 1
            else:
                current_yellow[letter] = 1
            valid_letters.add(letter)
        elif color == 'gray':
            grey_positions[i] = letter
            invalid_letters.add(letter)
    truly_incorrect = invalid_letters - valid_letters

    filtered_words = []
    for word in valid_words:
        word = word.lower()

        # Rule 1: match green positioning
        if any(word[i] != letter for i, letter in green_positions.items()):
            continue

        # Rule 2: exclude sole grey letters
        if any(til in word for til in truly_incorrect):
            continue

        # Rule 3: exclude secondary grey letters 
        if any(word[i] == letter for i, letter in grey_positions.items()):
            continue

        # Rule 4a: yellows cannot be in same position
        if any(word[i] == letter for i, letter in yellow_positions.items()):
            continue

        # Rule 4b: words with yellow characters in different positions 
        if any(word.count(letter) < count for letter, count in current_yellow.items()):
            continue

        filtered_words.append(word)
            
    return filtered_words

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
