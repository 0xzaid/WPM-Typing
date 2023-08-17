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
from rich.markdown import Markdown
from rich.layout import Layout


# COLORS CONSTANTS
CPURPLE = "\033[95m"
CRED = "\033[91m"
CEND = "\033[0m"
CGREEN = "\033[92m"
CBLUE = "\33[94m"

# INTEGER CONSTANTS
EASY_ROUND_LENGTH = 15
MEDIUM_ROUND_LENGTH = 45
HARD_ROUND_LENGTH = 70
CODE_ROUND_LENGTH = 120
ROUND_COUNTDOWN = 3
MIN_ACCURACY = 92
CODE_MIN_ACCURACY = 15

# TEXT CONSTANTS
EASY = "./data/easy.txt"
MEDIUM = "./data/medium.txt"
HARD = "./data/hard.txt"
CODE = "./data/code.txt"
MAX_CHAR_PER_LINE = 90
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
            choices=["1", "2", "3", "4", "m", "q"],
            show_default=True,
            show_choices=True,
        )

        # user_input = str(input("Choose gamemode using '1', '2' or 'q' to quit: "))

        if user_input == "1":
            clear()
            wpm(EASY)
        elif user_input == "2":
            wpm(MEDIUM)
        elif user_input == "3":
            wpm(HARD)
        elif user_input == "4":
            wpm(CODE)
        elif user_input == "q":
            clear()
            print(f"{CGREEN}Goodbye! Thanks for playing :){CEND}")
            sys.exit(1)
        elif user_input == "m":
            start_screen()
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
    # show_round_count()

    # show round time limit
    clear()
    show_round_time_limit(mode)

    # display phrases to user
    show_phrases(mode, phrase_to_type)

    # start countdown timer
    countdown_timer(ROUND_COUNTDOWN)

    # User starts typing, return the user's results and time
    result_typed, time_result = user_types(mode)

    # display the user's result and stats
    show_user_stats(mode, result_typed, phrase_to_type, time_result, word_count)


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
            Text(
                "Choose option: \n1. Easy\n2. Medium\n3. Hard\n4. Code\n m. Return to Main Menu\nq. Quit",
                justify="center",
            ),
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


def show_round_time_limit(mode):
    if mode == "./data/easy.txt":
        timing = EASY_ROUND_LENGTH
    elif mode == "./data/medium.txt":
        timing = MEDIUM_ROUND_LENGTH
    elif mode == "./data/hard.txt":
        timing = HARD_ROUND_LENGTH
    elif mode == "./data/code.txt":
        timing = CODE_ROUND_LENGTH

    panel = Panel(
        Text(
            f"You have {timing} seconds to complete this!",
            justify="center",
            style="green bold",
        ),
        border_style="blue",
    )
    rprint(panel)


def show_user_stats(mode, result_typed, phrase_to_type, time_result, word_count):
    # calculate percentage of similarity of typed phrase and given phrase and print stats
    min_accuracy = MIN_ACCURACY
    if mode == "./data/code.txt":
        min_accuracy = CODE_MIN_ACCURACY
    else:
        MIN_ACCURACY

    if similarity_percentage(result_typed, phrase_to_type) >= min_accuracy:
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
        Panel(Text(f"Accuracy too low to calculate! Try again", style="red bold"))
        # print(f"{CRED}Accuracy too low to calculate! Try again{CEND}")


def display_text(text, style=None):
    """
    Display text to the user in a customizable style.
    """
    round_count = str(len(ALL_WPMS) + 1)

    if style:
        text = Text(text, justify="center", style=style)
    else:
        text = Text(text, justify="center")

    text_panel = Panel(text, title=f"Round {round_count}", border_style="blue")
    rprint(text_panel)
    print()


def format_code(code):
    """
    Format code for display using Markdown.
    """
    code = replace_newlines_and_tabs(code)
    formatted_code = f"```python\n{code}\n```"
    markdown_code = Markdown(formatted_code)
    return markdown_code


def show_phrases(mode, phrase_to_type):
    """
    Display different types of phrases based on the mode.
    """
    
    round_count = str(len(ALL_WPMS) + 1)
    
    if mode in ["./data/medium.txt", "./data/hard.txt"]:
        phrase_to_type = max_characters_per_line(
            phrase_to_type
        )  # Assuming max_characters_per_line is defined

    if mode == "./data/code.txt":
        text = format_code(phrase_to_type)
        p = Panel(text, title=f"Round {round_count}", border_style="blue")
        rprint(p)
    else:
        text = f"{phrase_to_type}"
        display_text(text, style="purple" )


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
    elif mode == "./data/hard.txt":
        return HARD_ROUND_LENGTH
    elif mode == "./data/code.txt":
        return CODE_ROUND_LENGTH


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


def replace_newlines_and_tabs(input_text):
    output_text = input_text.replace("\\n", "\n").replace("\\t", "\t")
    return output_text


def main():
    start_screen()


if __name__ == "__main__":
    main()
