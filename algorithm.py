import math
import collections
from wordle import get_feedback
from collections import defaultdict, Counter

def load_words_from_file(filepath):
    """ 
    Creates a list of words from a .txt file. 
    """
    with open(filepath, 'r') as file:
        words = [line.strip().lower() for line in file]
    return words

def feedback_to_pattern(feedback):
    """
    Convert feedback format to internal pattern format with numerical values
    """
    mapping = {'gray': 0, 'yellow': 1, 'green': 2}
    return tuple(mapping[color] for color in feedback)

def get_feedback_pattern(guess, secret_word):
    """
    Get feedback pattern between guess and secret word
    """
    feedback = get_feedback(guess, secret_word)
    return feedback_to_pattern(feedback)

def calculate_entropy(guess, candidates):
    """
    Calculate expected information gain (entropy) for a guess
    """
    if not candidates:
        return 0
    # Count frequency of each possible feedback pattern
    pattern_counts = defaultdict(int)
    for candidate in candidates:
        pattern = get_feedback_pattern(guess, candidate)
        pattern_counts[pattern] += 1
    # Calculate entropy using slightly faster math
    entropy = 0
    total_candidates = len(candidates)
    log_total = math.log2(total_candidates) 
    for count in pattern_counts.values():
        if count > 0:
            probability = count / total_candidates
            entropy -= probability * (math.log2(count) - log_total)
    
    return entropy

def get_best_guess(candidates, all_words, max_guesses):
    """
    Find the guess that maximizes expected information gain
    """
    candidates_list = list(candidates)
    if len(candidates_list) <= 2:
        return candidates_list[0]
    # Use all words as potential guesses
    guess_pool = all_words
    
    # Limit guesses to check for speed
    if max_guesses and len(guess_pool) > max_guesses:
        # Mix remaining candidates with common starting words fir better efficiency
        common_starters = ['SLATE', 'TRACE', 'CRATE', 'ADIEU', 'AUDIO', 'ROATE', 'RAISE', 'STARE', 'CRANE', 'SLANT']
        guess_pool = list(candidates) + [w for w in common_starters if w in all_words]
        guess_pool = guess_pool[:max_guesses]
    best_guess = None
    best_entropy = -1
    for guess in guess_pool:
        entropy = calculate_entropy(guess, candidates_list)
        if entropy > best_entropy:
            best_entropy = entropy
            best_guess = guess  
    return best_guess

def filter_candidates(guess, feedback, candidates):
    """
    Filter candidates based on feedback from a guess
    feedback: list of ['gray', 'yellow', 'green']
    """
    target_pattern = feedback_to_pattern(feedback)
    new_candidates = set()
    for candidate in candidates:
        if get_feedback_pattern(guess, candidate) == target_pattern:
            new_candidates.add(candidate)
    return new_candidates

def make_next_guess(previous_guess, feedback, candidates, all_words):
    """
    Make the next optimal guess based on previous feedback
    Returns: (next_guess, updated_candidates)
    """
    # Filter candidates based on feedback
    new_candidates = filter_candidates(previous_guess, feedback, candidates)
    if len(new_candidates) == 1:
        return list(new_candidates)[0], new_candidates
    #Adjust max guesses depending on number of candidates
    if len(new_candidates) > 50:
        max_guesses = 300 
    elif len(new_candidates) > 10:
        max_guesses = 200
    else:
        max_guesses = None
    # Get best guess
    next_guess = get_best_guess(new_candidates, all_words, max_guesses)
    return next_guess, new_candidates