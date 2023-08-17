"""
A program that can measure words per minute when typing phrases 
"""

# Importing libraries
import random
import time
from difflib import SequenceMatcher
import os
import sys
from inputimeout import inputimeout

# Rich imports
from rich.panel import Panel
from rich import print as rprint
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from rich.layout import Layout


# COLORS CONSTANTS
CPURPLE = "\033[95m"
CRED = "\033[91m"
CEND = "\033[0m"
CGREEN = "\033[92m"
CBLUE = "\33[94m"

# INTEGER CONSTANTS
EASY_ROUND_LENGTH = 15
MEDIUM_ROUND_LENGTH = 60
ROUND_COUNTDOWN = 3
MIN_ACCURACY = 92

# TEXT CONSTANTS
EASY = "./data/easy.txt"
MEDIUM = "./data/medium.txt"
MAX_CHAR_PER_LINE = 85
user_input = ""

# ARRAY CONSTANTS
ALL_WPMS = []
CHOSEN_PHRASES = []


def start_screen():
    """
    Start screen text for user
    """
    console = Console()
    layout = setup_layout()
    show_welcome_message(layout)
    show_menu(layout)
    show_typers_legend(layout)
    show_footer(layout)
    rprint(layout)
    # print("Choose game mode: ")
    # print("1. Easy")
    # print("2. Medium")
    # print(CEND)

    while True:
        # user_input = ""

        p = Prompt()
        user_input = p.ask(
            prompt="Choose gamemode: \n ❯ ",
            console=Console(),
            choices=["1", "2", "q"],
            show_default=True,
            show_choices=True,
        )

        # user_input = str(input("Choose gamemode using '1', '2' or 'q' to quit: "))

        if user_input == "1":
            clear()
            wpm(EASY)
        elif user_input == "2":
            wpm(MEDIUM)
        elif user_input == "q":
            print(f"{CGREEN}Goodbye!{CEND}")
            clear()
            sys.exit(1)
        else:
            clear()
            print(f"{CRED}Incorrect input: {user_input}")
            print("Try again!")
        print(CEND)


def wpm(mode):
    # call load_phrase and store into ALL_PHRASES
    ALL_PHRASES = load_phrase(mode)

    # choose random phrase
    phrase_to_type = choose_phrase(ALL_PHRASES)

    # count number of words in phrase
    word_count = count_words_in_phrase(phrase_to_type)

    # show round count
    show_round_count()

    # display phrases to user
    show_phrases(mode, phrase_to_type)

    # start countdown timer
    countdown_timer(ROUND_COUNTDOWN)

    # User starts typing, return the user's results and time
    result_typed, time_result = user_types(mode)

    # display the user's result and stats
    show_user_stats(result_typed, phrase_to_type, time_result, word_count)


#################################################################################
"""
SHOW FUNCTIONS
"""
#################################################################################


def show_welcome_message(layout):
    # clear()
    # Create a Text element with the formatted time
    layout["upper"].update(
        Panel(
            Text(
                "Welcome to WPM Typer!",
                justify="center",
                style="green bold",
            ),
            border_style="green bold",
        )
    )

    # return layout
    # print(f"{CGREEN}------[Welcome to WPM type tester!]------")
    # print()


def show_menu(layout):
    layout["left"].update(
        Panel(
            Text("Choose game mode: \n1. Easy\n2. Medium\n", justify="center"),
            border_style="green bold",
            style="green bold",
        )
    )


def show_typers_legend(layout):
    def setup_table():
        # Title of the table
        table = Table(title="Typing Skill Level")

        # Adding columns
        table.add_column("Skill level", justify="center", style="cyan", no_wrap=True)
        table.add_column("WPM", justify="center", style="cyan", no_wrap=True)

        # Adding rows
        table.add_row("Beginner", "0-24")
        table.add_row("Intermediate", "25-30")
        table.add_row("Average", "31-41")
        table.add_row("Pro", "42-54")
        table.add_row("Typemaster", "55-79")
        table.add_row("Megaracer", "80+")
        return table

    table = setup_table()

    layout["right"].update(
        Panel(
            table,
            border_style="green bold",
        )
    )


def show_footer(layout):
    layout["footer"].update(
        Panel(
            Text(
                "Made with ❤️ by 0xzaid",
                justify="center",
                style="purple bold",
            ),
            border_style="green bold",
        )
    )


def show_round_count():
    round_count = str(len(ALL_WPMS) + 1)
    clear()
    print()
    panel = Panel(
        Text(
            f"[---------------------- Round {round_count} ----------------------]",
            justify="center",
            style="blue bold",
        ),
        border_style="blue",
    )
    rprint(panel)


def show_user_stats(result_typed, phrase_to_type, time_result, word_count):
    # calculate percentage of similarity of typed phrase and given phrase and print stats
    if similarity_percentage(result_typed, phrase_to_type) >= MIN_ACCURACY:
        clear()
        # print(f"{CGREEN}Statistics:")
        # print(
        #     str(round(similarity_percentage(result_typed, phrase_to_type), 1))
        #     + "% accuracy"
        # )
        # print(str(word_count) + " words in " + str(round(time_result, 1)) + " seconds")
        WPM = round((word_count / time_result) * 60, 1)
        # print(f"Your WPM is: {str(WPM)}")

        round_count = str(len(ALL_WPMS) + 1)

        ALL_WPMS.append(WPM)

        avg = average(ALL_WPMS)

        p = Panel(
            Text(
                f"""Your Accuracy was: {str(round(similarity_percentage(result_typed, phrase_to_type), 1))}%\nYour WPM score is: {str(WPM)}\nAfter {round_count} rounds, your average is: {avg}""",
                style="bold green",
                justify="center",
            ),
            title="Statistics",
            border_style="purple bold",
        )
        rprint(p)

        # print(f"Your average WPM is: {str(average(ALL_WPMS))}{CEND}")
    else:
        Panel(Text(f"Accuracy too low to calculate! Try again"))
        # print(f"{CRED}Accuracy too low to calculate! Try again{CEND}")


def show_phrases(mode, phrase_to_type):
    """
    display text to user
    """
    # if mode is medium
    if mode == "./data/medium.txt":
        # improving readability by limiting char count per line
        phrase_to_type = max_characters_per_line(phrase_to_type)

    panel = Panel(
        Text(f"{phrase_to_type}", justify="center", style="purple"), border_style="blue"
    )
    rprint(panel)
    # print(CPURPLE + phrase_to_type + CEND)
    print()


#################################################################################
"""
RICH FUNCTIONS
"""
#################################################################################


def setup_layout():
    layout = Layout()

    # initializing sections in layout
    layout.split_column(
        Layout(name="upper"),
        Layout(name="lower"),
        Layout(name="footer"),
    )

    # setting sizes
    layout["upper"].size = 3
    layout["lower"].size = 16
    layout["footer"].size = 3

    # layout['lower'].size = 16
    layout["lower"].split_row(
        Layout(name="left", ratio=2),
        Layout(name="right", ratio=1),
    )

    return layout
    # rprint(layout)


#################################################################################
"""
OTHER WPM FUNCTIONS
"""
#################################################################################


def user_types(mode):
    # start timer
    start = time.time()
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

    time_result = end - start

    return result_typed, time_result


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
    Choose a random phrase from the phrases list
    It keeps track that a phrase has not been chosen
    previously in the game
    """
    while True:
        # Get a phrase
        current_phrase = random.choice(phrases_list)
        # If not seen before, add to list and return
        # else get a another phrase
        if current_phrase not in CHOSEN_PHRASES:
            CHOSEN_PHRASES.append(current_phrase)
            return current_phrase


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
    if mode == "./data/easy.txt":
        return EASY_ROUND_LENGTH
    elif mode == "./data/medium.txt":
        return MEDIUM_ROUND_LENGTH


def average(a_list):
    """
    return average of a list
    """
    length = len(a_list)
    if length == 0:
        return
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
        countdown_text = Text(str(i), style="bold red")
        countdown_panel = Panel(countdown_text, expand=False, border_style="bold red")

        # Print the countdown panel on the same line without clearing
        rprint(countdown_panel, end="\r=")
        time.sleep(1)

    # Clear the line by printing spaces and moving the cursor back
    # print(" " * len(str(seconds)), end="\r")
    sys.stdout.flush()


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


if __name__ == "__main__":
    main()
