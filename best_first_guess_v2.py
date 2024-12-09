from collections import defaultdict
import math

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

# Function to find the best first guess
# Picks the first guess that minimizes the size of XXXXX feedback category.
def best_first_guess(word_list):
    # Dictionary to store the best guess and its information gain
    best_guess = None
    best_feedback_dist = None
    best_score = 10000000

    # Iterate over each word in the word list
    for guess in word_list:
        # Dictionary to count feedback distributions
        feedback_distribution = defaultdict(int)
        print(f"getting feedback dist for {guess}")

        # Compare the guess with every other word in the list
        for target in word_list:
            feedback = get_feedback(guess, target)
            feedback_distribution[feedback] += 1

        score = feedback_distribution['XXXXX']
        # Check if this guess is better (fewer XXXXX feedback than the current best guess)
        if score < best_score:
            best_score = score
            best_guess = guess
            best_feedback_dist = feedback_distribution

    return best_guess, best_feedback_dist

# Example usage
word_list = read_dictionary()
# word_list = ['apple', 'brick', 'flame', 'clamp', 'grape', 'sheen', 'stone']

best_guess, feedback = best_first_guess(word_list)
print("Best first guess:", best_guess)
print(feedback)
