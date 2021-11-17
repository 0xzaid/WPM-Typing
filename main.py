"""
A program that can measure words per minute when typing phrases 
"""

def start_screen():
    pass

def display_text():
    pass

def load_phrases():
    """
    Reads phrases from a file called phrases.txt for user to write in terminal to practice
    """
    all_phrases = ""
    f = open("phrases.txt", "r")
    lines = f.readlines()
    for line in lines:
        all_phrases += line
    print(all_phrases)

def wpm():
    pass

def main():
    load_phrases()

if __name__ == '__main__':
    main()