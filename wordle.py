from typing import List

# Only get words of this length
WORD_LENGTH = 5

# Get this many words
WORD_COUNT = 5

# Read dictionary
def read_dictionary():
    with open('csw19.txt', 'r') as f:
        l = f.readlines()
        l = [x[:-1].lower() for x in l]
    return set(l)

def get_num_letters(word_list):
    return len(set(''.join(word_list)))

def trim_words_with_dup_letters(word_list):
    output = []
    for word in word_list:
        if get_num_letters([word]) == len(word):
            output.append(word)
    return output

def filter_out_overlapping_words(curr_words, words_list):
    output = [x for x in words_list if get_num_letters([x] + curr_words) == WORD_LENGTH * (len(curr_words) + 1)]
    return output

def update_state(curr_state, words_to_guess):
    output = curr_state
    for i in range(len(output)-1, -1, -1):
        if output[i] >= len(words_to_guess[i]):
            rem = output[i] - len(words_to_guess[i])
            if i != 0:
                output[i-1] += 1
            output[i] = rem
    return output

def trim_words_with_two_vowels(words_list):
    vowels = ['a', 'e', 'i', 'o', 'u']
    output = [x for x in words_list if get_num_letters([x] + vowels) >= len(x) + 4]
    return output

def score_solution(soln, words_list):
    tally = 0
    for x in soln:
        for w in words_list:
            for i in range(WORD_LENGTH):
                if x[i] == w[i]:
                    tally += 1
    return tally

def main():
    words = read_dictionary()
    words = [x for x in words if len(x) == WORD_LENGTH]
    full_dict = words
    words = trim_words_with_dup_letters(words)
    # words = trim_words_with_two_vowels(words)
    words = sorted(words)

    print(len(words))

    initial_state = [0]
    words_to_guess = [words]
    curr_state = initial_state

    solutions = []
    iteration = 0

    while curr_state[0] < len(words_to_guess[0]):
        current_depth = len(curr_state)
        current_words = [words_to_guess[i][j] for i, j in enumerate(curr_state)]

        if iteration % 5000 == 0:
            print(current_words)

        if current_depth == WORD_COUNT:
            print(current_words)
            print(get_num_letters(current_words))
            solutions.append(current_words)

        next_words_to_guess = filter_out_overlapping_words(current_words, words_to_guess[current_depth-1][curr_state[-1]:])
        if len(next_words_to_guess) == 0:
            curr_state[-1] += 1
            if curr_state[-1] >= len(words_to_guess[-1]):
                curr_state = curr_state[:-1]
                words_to_guess = words_to_guess[:-1]
                if len(curr_state) == 0:
                    break
                curr_state[-1] += 1
                curr_state = update_state(curr_state, words_to_guess)
        else:
            curr_state.append(0)
            words_to_guess.append(next_words_to_guess)

        iteration += 1

    print("\n\nNumber of groupings tried: ", iteration)
    for soln in solutions:
        print(soln, " ", score_solution(soln, full_dict))

if __name__ == "__main__":
    main()
