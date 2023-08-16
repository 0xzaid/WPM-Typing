"""
A program that can measure words per minute when typing phrases 
"""
import random
import time
from difflib import SequenceMatcher
import os
import sys
from inputimeout import inputimeout

# colors for text
CPURPLE = "\033[95m"
CRED = "\033[91m"
CEND = "\033[0m"
CGREEN = "\033[92m"
CBLUE = "\33[94m"

# keep track of all wpms
all_wpms = []

# CONSTANTS
EASY_ROUND_LENGTH = 15
MEDIUM_ROUND_LENGTH = 60
ROUND_COUNTDOWN = 3
MIN_ACCURACY = 92
EASY = "./data/easy.txt"
MEDIUM = "./data/medium.txt"
MAX_CHAR_PER_LINE = 100


def start_screen():
    """
    Start screen text for user
    """
    clear()
    print(f"{CGREEN}------[Welcome to WPM type tester!]------")
    print()
    # print(" - Text will be displayed")
    print("Choose game mode: ")
    print("1. Easy")
    print("2. Medium")
    # print(" - whenever ready type r click enter and a timer will start" + CEND)
    print(CEND)

    while True:
        print(CGREEN)
        game_mode = str(input("Choose gamemode using '1', '2' or 'q' to quit: "))

        if game_mode == "1":
            clear()
            wpm(EASY)
        elif game_mode == "2":
            wpm(MEDIUM)
        elif ready == "q":
            print(CGREEN + "Goodbye!" + CEND)
            clear()
            sys.exit(1)
        else:
            clear()
            print(CRED + "Incorrect input: " + game_mode)
            print("Try again!")
            print(CEND)


def wpm(mode):
    # call load_phrase and store into  ALL_PHRASES
    ALL_PHRASES = load_phrase(mode)

    # choose random phrase
    phrase_to_type = choose_phrase(ALL_PHRASES)

    # count number of words in phrase
    word_count = count_words_in_phrase(phrase_to_type)

    # show round count
    clear()
    print()
    print(CBLUE)
    print(
        f"[---------------------- Round {str(len(all_wpms) + 1)} ----------------------]"
    )
    print(CEND)

    # display phrases to user
    display_phrases(mode, phrase_to_type)

    # start countdown timer
    countdown_timer(ROUND_COUNTDOWN)

    # start timer
    start = time.time()
    # result_typed = str(input())

    round_length = get_round_length(mode)

    try:
        # Take timed input using inputimeout() function
        result_typed = str(inputimeout(prompt="", timeout=round_length))

    # Catch the timeout error
    except Exception:
        # Declare the timeout statement
        time_over = "You took too long!"
        print(time_over)
        sys.exit(1)

    # end timer
    end = time.time()

    # calculate percentage of similarity of typed phrase and given phrase and print stats
    if similarity_percentage(result_typed, phrase_to_type) >= MIN_ACCURACY:
        time_result = end - start
        clear()
        print(f"{CGREEN}Statistics:")
        print(
            str(round(similarity_percentage(result_typed, phrase_to_type), 1))
            + "% accuracy"
        )
        # print(str(word_count) + " words in " + str(round(time_result, 1)) + " seconds")
        WPM = round((word_count / time_result) * 60, 1)
        print(f"Your WPM is: {str(WPM)}")
        all_wpms.append(WPM)

        print(f"Your average WPM is: {str(average(all_wpms))}{CEND}")
    else:
        print(f"{CRED}Accuracy too low to calculate! Try again{CEND}")


def display_phrases(mode, phrase_to_type):
    """
    display text to user
    """
    # if mode is medium

    if mode == "medium.txt":
        # improving readability by limiting char count per line
        phrase_to_type = max_characters_per_line(phrase_to_type)

    print(CPURPLE + phrase_to_type + CEND)
    print()


def load_phrase(mode):
    """
    Reads phrases from a file called phrases.txt for user to write in terminal to practice
    """
    all_phrases = ""
    with open(mode) as f:
        all_phrases = f.read().splitlines()
    return all_phrases


def choose_phrase(phrases_list):
    """
    Choose a random phrase from the phrases lsit
    """
    return random.choice(phrases_list)


def count_words_in_phrase(phrase_to_type):
    """
    return count number of words in a phrase
    """
    return len(phrase_to_type.split())


#################################################################################
"""
 UTILITY FUNCTIONS AND VARIABLES
"""
#################################################################################
# clear console
# different for windows or linux
if os.name == "nt":
    clear = lambda: os.system("cls")
else:
    clear = lambda: os.system("clear")


def get_round_length(mode):
    if mode == 1:
        return EASY_ROUND_LENGTH
    elif mode == 2:
        return MEDIUM_ROUND_LENGTH


def average(a_list):
    """
    return average of a list
    """
    length = len(a_list)
    return round(sum(a_list) / length, 1)


def similarity_percentage(a, b):
    """
    calculate similarity percentage between two strings
    """
    return SequenceMatcher(None, a, b).ratio() * 100


def countdown_timer(seconds):
    """
    countdown timer based on 'seconds' variable
    """
    for i in range(seconds, 0, -1):
        print(str(i), end="\r")
        time.sleep(1)

    # Clear the line by printing spaces and moving the cursor back
    print(" " * len(str(seconds)), end="\r")
    sys.stdout.flush()


def format_into_lines_of_10_words(phrase):
    """
    A function that returns a long sentences into multiple lines for better readability.
    Each line must have max 10 words, then we add a new line and continue.
    """
    words = phrase.split()
    lines = []

    for i in range(0, len(words), 10):
        line = " ".join(words[i : i + 10])
        lines.append(line)

    return "\n".join(lines)


def max_characters_per_line(phrase, max_characters=MAX_CHAR_PER_LINE):
    """
    A function that returns a long sentences into multiple lines based on a max amount of characters
    for better readability.
    Each line must have max 10 words, then we add a new line and continue.
    """
    words = phrase.split()
    lines = []
    current_line = []

    for word in words:
        if current_line and len(" ".join(current_line + [word])) > max_characters:
            lines.append(" ".join(current_line))
            current_line = [word]
        else:
            current_line.append(word)

    if current_line:
        lines.append(" ".join(current_line))

    return "\n".join(lines)


def main():
    start_screen()
    # print(format_into_lines_of_10_words("Under the star-studded canopy of the night sky, a lone astronomer peered through a telescope, captivated by the distant galaxies and nebulae that painted a tapestry of cosmic wonder."))


if __name__ == "__main__":
    main()
