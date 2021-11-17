"""
A program that can measure words per minute when typing phrases 
"""

def start_screen():
    """
    Start screen text for user
    """
    print("------[Welcome to WPM type tester!]------")
    print()
    print(" - Text will be displayed")
    print(" - whenever ready type r click enter and a timer will start")


def display_phrases():
    """
    display text to user
    """
    pass

def load_phrase():
    """
    Reads phrases from a file called phrases.txt for user to write in terminal to practice
    """
    all_phrases = ""
    f = open("phrases.txt", "r")
    lines = f.readlines()
    for line in lines:
        all_phrases += line
    

def wpm():
    pass

def main():
    start_screen()
    # load_phrases()

if __name__ == '__main__':
    main()