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
ROUND_LENGTH = 15
ROUND_COUNTDOWN = 3
MIN_ACCURACY = 92


def start_screen():
    """
    Start screen text for user
    """
    clear()
    print(CGREEN + "------[Welcome to WPM type tester!]------")
    print()
    print(" - Text will be displayed")
    print(" - whenever ready type r click enter and a timer will start" + CEND)

    while True:
        print(CGREEN)
        ready = str(input("Enter 'r' when ready or 'q' to quit: "))
        print(CEND)
        if ready == "r":
            clear()
            wpm()
        elif ready == "q":
            print(CGREEN + "Goodbye!" + CEND)
            clear()
            sys.exit(1)
        else:
            print(CRED + "Incorrect input: you input " + ready + " and not 'r' " + CEND)


def display_phrases(phrase_to_type):
    """
    display text to user
    """
    print(CPURPLE + "[---- " + phrase_to_type + " ----]" + CEND)
    print()


def load_phrase():
    """
    Reads phrases from a file called phrases.txt for user to write in terminal to practice
    """
    all_phrases = ""
    with open("data.txt") as f:
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


def wpm():
    # call load_phrase and store into  ALL_PHRASES
    ALL_PHRASES = load_phrase()

    # choose random phrase
    phrase_to_type = choose_phrase(ALL_PHRASES)

    # count number of words in phrase
    word_count = count_words_in_phrase(phrase_to_type)
    
    # show round count
    print()
    print(CBLUE)
    print("[---------------------- Round " + str(len(all_wpms)+1) + " ----------------------]")
    print(CEND)

    # display phrases to user
    display_phrases(phrase_to_type)

    # start countdown timer
    countdown_timer(ROUND_COUNTDOWN)

    # start timer
    start = time.time()
    # result_typed = str(input())

    try:
        # Take timed input using inputimeout() function
        result_typed = str(inputimeout(prompt="", timeout=ROUND_LENGTH))

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
        print(CGREEN + "Statistics:")
        print(
            str(round(similarity_percentage(result_typed, phrase_to_type), 1))
            + "% accuracy"
        )
        # print(str(word_count) + " words in " + str(round(time_result, 1)) + " seconds")
        WPM = round((word_count / time_result) * 60, 1)
        print("Your WPM is: " + str(WPM))
        all_wpms.append(WPM)

        print("Your average WPM is: " + str(average(all_wpms)) + CEND)
    else:
        print(CRED + "Accuracy too low to calculate! Try again" + CEND)


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


def main():
    start_screen()


if __name__ == "__main__":
    main()
