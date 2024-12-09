from collections import defaultdict
import math
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, cpu_count

# Only get words of this length
WORD_LENGTH = 5

# Get this many words
WORD_COUNT = 5

# Read dictionary
def read_dictionary():
    with open('csw19.txt', 'r') as f:
        l = f.readlines()
        l = [x[:-1].lower() for x in l]
        l = [x for x in l if len(x) == WORD_LENGTH]
    return l

# Function to simulate the feedback of Wordle
def get_feedback(guess, target):
    feedback = []
    target_list = list(target)
    guess_list = list(guess)

    # First pass: mark all green (correct letters in the correct position)
    for i in range(5):
        if guess_list[i] == target_list[i]:
            feedback.append('G')  # 'G' for green
            target_list[i] = None  # Remove from target to avoid reusing this letter
            guess_list[i] = None  # Remove from guess
        else:
            feedback.append(None)

    # Second pass: mark yellow (correct letter, wrong position)
    for i in range(WORD_LENGTH):
        if feedback[i] is None and guess_list[i] is not None:
            if guess_list[i] in target_list:
                feedback[i] = 'Y'  # 'Y' for yellow
                target_list[target_list.index(guess_list[i])] = None  # Remove the letter
            else:
                feedback[i] = 'X'  # 'X' for gray (not in word)
    return ''.join(feedback)

def is_consistent_with_feedback(guess, feedback, target):
    guess_list = list(guess)
    target_list = list(target)
    for i in range(WORD_LENGTH):
        if feedback[i] == 'G' and guess_list[i] != target_list[i]:
            return False
        if feedback[i] == 'X' and guess_list[i] in target_list:
            return False
        if feedback[i] == 'Y' and (guess_list[i] not in target_list or guess_list[i] == target_list[i]):
            return False
    return True

def count_words_consistent_with_feedback(guess, feedback, word_list):
    count = 0
    for target in word_list:
        if is_consistent_with_feedback(guess, feedback, target):
            count += 1
    return count

def best_first_guess(word_list):
    """
    Find the best first guess that minimizes the quantity of remaining hardcore mode words.

    Args:
        word_list (list): List of words to consider.

    Returns:
        tuple: Best guess and the average number of valid words left.
    """
    best_guess = None
    best_score = None
    best_num_valid_guesses = 350 * len(word_list)

    with Pool(processes=cpu_count()) as pool:
        results = pool.starmap(process_guess, [(word_list[i], word_list) for i in range(len(word_list))])

    for initial_guess, num_valid_guesses in results:
        if best_score is None or num_valid_guesses < best_score:
            best_score = num_valid_guesses
            best_guess = initial_guess
            best_num_valid_guesses = num_valid_guesses

    return best_guess, best_num_valid_guesses / len(word_list)

def process_guess(initial_guess, word_list):
    num_valid_guesses = 0
    feedback_cache = {}
    for target in word_list:
        feedback = get_feedback(initial_guess, target)
        if feedback in feedback_cache:
            num_valid_guesses += feedback_cache[feedback]
        else:
            feedback_num_guesses = count_words_consistent_with_feedback(
                initial_guess, feedback, word_list)
            feedback_cache[feedback] = feedback_num_guesses
            num_valid_guesses += feedback_num_guesses
    print(f"initial guess: {initial_guess}, num valid guesses: "
          f"{num_valid_guesses / len(word_list)}")
    return initial_guess, num_valid_guesses

if __name__ == '__main__':
    # Example usage
    word_list = read_dictionary()
    # word_list = ['apple', 'brick', 'flame', 'clamp', 'grape', 'sheen', 'stone']

    best_guess, best_avg_num_valid_guesses = best_first_guess(word_list)
    print("Best first guess:", best_guess)
    print("Average number of valid words left:", best_avg_num_valid_guesses)
