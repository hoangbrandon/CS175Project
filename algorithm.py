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

def calculate_entropy(guess, candidates):
    """
    Calculate expected information gain (entropy) for a guess
    """
    if not candidates:
        return 0
    # Count frequency of each possible feedback pattern
    pattern_counts = defaultdict(int)
    for candidate in candidates:
        feedback = get_feedback(guess, candidate)
        pattern = feedback_to_pattern(feedback)
        pattern_counts[pattern] += 1
    
    # Calculate entropy
    entropy = 0
    total_candidates = len(candidates)
    for count in pattern_counts.values():
        if count > 0:
            probability = count / total_candidates
            entropy -= probability * math.log2(probability)
    return entropy

def get_best_guess(candidates, all_words):
    """
    Find the guess that maximizes expected information gain
    """
    if len(candidates) <= 2:
        # If only 1-2 candidates left, just guess one of them
        return list(candidates)[0]
    best_guess = None
    best_entropy = -1
    guess_pool = all_words
    # Calculate entropy for all words in guess pool
    for guess in guess_pool:
        entropy = calculate_entropy(guess, candidates)
        if entropy > best_entropy:
            best_entropy = entropy
            best_guess = guess
    return best_guess

def filter_candidates(guess, feedback, candidates):
    """
    Filter candidates based on feedback from a guess
    feedback: list of ['gray', 'yellow', 'green']
    """
    new_candidates = set()
    target_pattern = feedback_to_pattern(feedback)
    for candidate in candidates:
        candidate_feedback = get_feedback(guess, candidate)
        candidate_pattern = feedback_to_pattern(candidate_feedback)
        if candidate_pattern == target_pattern:
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
    # Get best guess
    next_guess = get_best_guess(new_candidates, all_words)
    return next_guess, new_candidates