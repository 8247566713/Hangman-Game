
"""
=============================================================================
Project Name   : Rich Text-Based Hangman Game
Task           : CodeAlpha Task-1 (Python Programming)
Description    : An interactive console-based Hangman game where the player
                 guesses a hidden word one letter at a time. Designed with
                 rich terminal aesthetics, ASCII art gallows, ANSI colors,
                 session stats, and robust input validation.
Key Concepts   : random, while loops, if-else statements, strings, lists
Author         : Python Developer
=============================================================================
"""

import os
import sys
import random
import time

# Ensure UTF-8 output encoding for modern terminal symbols & emojis on Windows
if sys.platform.startswith("win"):
    os.system("")  # Enables ANSI Virtual Terminal processing in Windows cmd/powershell
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdin.reconfigure(encoding="utf-8")
    except AttributeError:
        pass


# =============================================================================
# ANSI COLOR THEME & STYLING (Rich Terminal Aesthetics without 3rd-party dependencies)
# =============================================================================
class Style:
    RESET       = "\033[0m"
    BOLD        = "\033[1m"
    DIM         = "\033[2m"
    UNDERLINE   = "\033[4m"

    # Foreground colors
    BLACK       = "\033[30m"
    RED         = "\033[91m"
    GREEN       = "\033[92m"
    YELLOW      = "\033[93m"
    BLUE        = "\033[94m"
    MAGENTA     = "\033[95m"
    CYAN        = "\033[96m"
    WHITE       = "\033[97m"
    GRAY        = "\033[90m"

    # Background colors
    BG_RED      = "\033[41m"
    BG_GREEN    = "\033[42m"
    BG_BLUE     = "\033[44m"


# =============================================================================
# PREDEFINED WORDS & HINTS (Scope Requirement: Exactly 5 predefined words)
# =============================================================================
WORD_COLLECTION = [
    {
        "word": "PYTHON",
        "category": "Technology",
        "hint": "A versatile programming language named after a British comedy troupe."
    },
    {
        "word": "GALAXY",
        "category": "Astronomy",
        "hint": "A gravitationally bound system of stars, stellar remnants, and dark matter."
    },
    {
        "word": "WIZARD",
        "category": "Fantasy",
        "hint": "A wise practitioner of magic and master of mystical ancient arts."
    },
    {
        "word": "JUNGLE",
        "category": "Nature",
        "hint": "A dense, tropical forest teeming with wild vegetation and biodiversity."
    },
    {
        "word": "SHADOW",
        "category": "Science",
        "hint": "A dark shape formed on a surface when light is blocked by an object."
    }
]

MAX_INCORRECT_GUESSES = 6  # Limit to 6 incorrect guesses as per task scope


# =============================================================================
# ASCII ART: GALLOWS STAGES (0 to 6 Mistakes)
# =============================================================================
HANGMAN_STAGES = [
    # 0 Mistakes: Empty Gallows
    f"""
       {Style.BLUE}+---+{Style.RESET}
       {Style.BLUE}|   |{Style.RESET}
           {Style.BLUE}|{Style.RESET}
           {Style.BLUE}|{Style.RESET}
           {Style.BLUE}|{Style.RESET}
           {Style.BLUE}|{Style.RESET}
    {Style.CYAN}========={Style.RESET}
    """,
    # 1 Mistake: Head
    f"""
       {Style.BLUE}+---+{Style.RESET}
       {Style.BLUE}|   |{Style.RESET}
       {Style.YELLOW}O{Style.RESET}   {Style.BLUE}|{Style.RESET}
           {Style.BLUE}|{Style.RESET}
           {Style.BLUE}|{Style.RESET}
           {Style.BLUE}|{Style.RESET}
    {Style.CYAN}========={Style.RESET}
    """,
    # 2 Mistakes: Head and Torso
    f"""
       {Style.BLUE}+---+{Style.RESET}
       {Style.BLUE}|   |{Style.RESET}
       {Style.YELLOW}O{Style.RESET}   {Style.BLUE}|{Style.RESET}
       {Style.WHITE}|{Style.RESET}   {Style.BLUE}|{Style.RESET}
           {Style.BLUE}|{Style.RESET}
           {Style.BLUE}|{Style.RESET}
    {Style.CYAN}========={Style.RESET}
    """,
    # 3 Mistakes: Left Arm
    f"""
       {Style.BLUE}+---+{Style.RESET}
       {Style.BLUE}|   |{Style.RESET}
       {Style.YELLOW}O{Style.RESET}   {Style.BLUE}|{Style.RESET}
      {Style.WHITE}/|{Style.RESET}   {Style.BLUE}|{Style.RESET}
           {Style.BLUE}|{Style.RESET}
           {Style.BLUE}|{Style.RESET}
    {Style.CYAN}========={Style.RESET}
    """,
    # 4 Mistakes: Right Arm
    f"""
       {Style.BLUE}+---+{Style.RESET}
       {Style.BLUE}|   |{Style.RESET}
       {Style.YELLOW}O{Style.RESET}   {Style.BLUE}|{Style.RESET}
      {Style.WHITE}/|\\{Style.RESET}  {Style.BLUE}|{Style.RESET}
           {Style.BLUE}|{Style.RESET}
           {Style.BLUE}|{Style.RESET}
    {Style.CYAN}========={Style.RESET}
    """,
    # 5 Mistakes: Left Leg
    f"""
       {Style.BLUE}+---+{Style.RESET}
       {Style.BLUE}|   |{Style.RESET}
       {Style.YELLOW}O{Style.RESET}   {Style.BLUE}|{Style.RESET}
      {Style.WHITE}/|\\{Style.RESET}  {Style.BLUE}|{Style.RESET}
      {Style.WHITE}/{Style.RESET}    {Style.BLUE}|{Style.RESET}
           {Style.BLUE}|{Style.RESET}
    {Style.CYAN}========={Style.RESET}
    """,
    # 6 Mistakes: Right Leg (Dead)
    f"""
       {Style.RED}+---+{Style.RESET}
       {Style.RED}|   |{Style.RESET}
       {Style.RED}X{Style.RESET}   {Style.RED}|{Style.RESET}
      {Style.RED}/|\\{Style.RESET}  {Style.RED}|{Style.RESET}
      {Style.RED}/ \\{Style.RESET}  {Style.RED}|{Style.RESET}
           {Style.RED}|{Style.RESET}
    {Style.RED}========={Style.RESET}
    """
]


# =============================================================================
# HELPER FUNCTIONS & UI RENDERERS
# =============================================================================
def clear_screen():
    """Clears the console screen across Windows and Unix platforms."""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    """Displays the stylish top banner for the Hangman game."""
    banner = f"""
{Style.CYAN}{Style.BOLD}╔═══════════════════════════════════════════════════════════╗
║                  ★  H A N G M A N  ★                      ║
║            Classic Text-Based Word Guessing Game          ║
║               CodeAlpha Python Project Task-1             ║
╚═══════════════════════════════════════════════════════════╝{Style.RESET}
"""
    print(banner)


def display_health_bar(incorrect_count, max_lives):
    """
    Renders an ASCII health bar indicating remaining lives.
    Key Concept: strings and math formatting.
    """
    remaining_lives = max_lives - incorrect_count
    bar_symbols = ""
    for i in range(max_lives):
        if i < remaining_lives:
            bar_symbols += f"{Style.GREEN}■ {Style.RESET}"
        else:
            bar_symbols += f"{Style.RED}✖ {Style.RESET}"

    color = Style.GREEN if remaining_lives >= 4 else (Style.YELLOW if remaining_lives >= 2 else Style.RED)
    print(f"  {Style.BOLD}Lives Remaining:{Style.RESET} [ {bar_symbols}] {color}({remaining_lives}/{max_lives}){Style.RESET}")


def display_alphabet_tracker(guessed_letters, secret_word):
    """
    Displays the alphabet letter bank with visual status:
    - Green  : Correctly guessed letter
    - Red    : Incorrectly guessed letter
    - Dim/Gray : Available unguessed letter
    Key Concept: strings and loops.
    """
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    display_letters = []

    for char in alphabet:
        if char in guessed_letters:
            if char in secret_word:
                # Correct letter
                display_letters.append(f"{Style.GREEN}{Style.BOLD}{char}{Style.RESET}")
            else:
                # Wrong letter
                display_letters.append(f"{Style.RED}{Style.DIM}{char}{Style.RESET}")
        else:
            # Unguessed letter
            display_letters.append(f"{Style.GRAY}{char}{Style.RESET}")

    print(f"\n  {Style.BOLD}Letter Bank:{Style.RESET} " + " ".join(display_letters))


def get_masked_word(secret_word, guessed_letters):
    """
    Returns the word representation with revealed letters and underscores.
    Key Concept: lists, strings, and if-else.
    """
    revealed_list = []
    for letter in secret_word:
        if letter in guessed_letters:
            revealed_list.append(f"{Style.CYAN}{Style.BOLD}{letter}{Style.RESET}")
        else:
            revealed_list.append(f"{Style.WHITE}_{Style.RESET}")
    return " ".join(revealed_list)


# =============================================================================
# CORE GAMEPLAY FUNCTION
# =============================================================================
def play_hangman(stats):
    """
    Runs a single round of Hangman.
    Demonstrates:
    - random module: picking random secret word
    - while loop: turn-by-turn game loop
    - if-else statements: handling guess states
    - strings & lists: tracking letters and word states
    """
    # 1. Randomly select a word item from the 5 predefined words
    chosen_item = random.choice(WORD_COLLECTION)
    secret_word = chosen_item["word"]
    category = chosen_item["category"]
    hint = chosen_item["hint"]

    # 2. Initialize tracking lists and counters
    guessed_letters = []       # List of all guessed letters
    incorrect_guesses = 0      # Counter of wrong attempts (Max: 6)
    hint_revealed = False      # Player can ask for hint
    feedback_message = f"{Style.CYAN}Game started! Guess your first letter.{Style.RESET}"

    # 3. Main Game Loop (while loop)
    while incorrect_guesses < MAX_INCORRECT_GUESSES:
        clear_screen()
        print_banner()

        # Display Category Badge
        print(f"  {Style.BOLD}Category:{Style.RESET} {Style.MAGENTA}[{category}]{Style.RESET}   |   {Style.BOLD}Word Length:{Style.RESET} {len(secret_word)} letters")

        # Display Gallows Graphic (list index corresponds to incorrect guesses)
        print(HANGMAN_STAGES[incorrect_guesses])

        # Display Health / Remaining Lives
        display_health_bar(incorrect_guesses, MAX_INCORRECT_GUESSES)

        # Display Masked Secret Word
        print(f"\n  {Style.BOLD}Current Word:{Style.RESET}  {get_masked_word(secret_word, guessed_letters)}\n")

        # Display Letter Bank Tracker
        display_alphabet_tracker(guessed_letters, secret_word)

        # Display Hint status if revealed
        if hint_revealed:
            print(f"\n  {Style.YELLOW}{Style.BOLD}💡 Hint:{Style.RESET} {Style.YELLOW}{hint}{Style.RESET}")
        else:
            print(f"\n  {Style.GRAY}(Type '?' at any time to reveal a hint){Style.RESET}")

        # Display feedback from previous action
        print(f"\n  {Style.BOLD}Status:{Style.RESET} {feedback_message}\n")

        # Check Win Condition: Have all letters in secret_word been guessed?
        all_revealed = True
        for letter in secret_word:
            if letter not in guessed_letters:
                all_revealed = False
                break

        if all_revealed:
            # Player Won!
            stats["wins"] += 1
            stats["streak"] += 1
            print(f"  {Style.BG_GREEN}{Style.WHITE}{Style.BOLD} ★ CONGRATULATIONS! YOU WON! ★ {Style.RESET}")
            print(f"  You successfully identified the word: {Style.GREEN}{Style.BOLD}{secret_word}{Style.RESET}")
            print(f"  Mistakes made: {incorrect_guesses}/{MAX_INCORRECT_GUESSES}\n")
            return

        # 4. Prompt for user input
        user_input = input(f"  {Style.CYAN}Enter a letter guess >> {Style.RESET}").strip().upper()

        # 5. Input Validation & Processing using if-else structures
        if user_input == "?":
            # Hint requested
            if not hint_revealed:
                hint_revealed = True
                feedback_message = f"{Style.YELLOW}Hint revealed above!{Style.RESET}"
            else:
                feedback_message = f"{Style.YELLOW}Hint is already shown.{Style.RESET}"
            continue

        if len(user_input) != 1:
            # Invalid input length
            feedback_message = f"{Style.RED}⚠ Please enter exactly ONE letter at a time.{Style.RESET}"
            continue

        if not user_input.isalpha():
            # Invalid character (number or punctuation)
            feedback_message = f"{Style.RED}⚠ Invalid character. Only letters A-Z are accepted.{Style.RESET}"
            continue

        if user_input in guessed_letters:
            # Duplicate guess
            feedback_message = f"{Style.YELLOW}ℹ You already guessed '{user_input}'. Try a different letter!{Style.RESET}"
            continue

        # Add guess to the list of guessed letters
        guessed_letters.append(user_input)

        # Check if the guessed letter is inside the secret word
        if user_input in secret_word:
            occurrences = secret_word.count(user_input)
            feedback_message = f"{Style.GREEN}✔ Good job! '{user_input}' is in the word! ({occurrences} found){Style.RESET}"
        else:
            incorrect_guesses += 1
            remaining = MAX_INCORRECT_GUESSES - incorrect_guesses
            feedback_message = f"{Style.RED}✖ Oops! '{user_input}' is NOT in the word. ({remaining} lives left){Style.RESET}"

    # 6. Loss Condition (while loop finished because incorrect_guesses == 6)
    clear_screen()
    print_banner()
    print(HANGMAN_STAGES[MAX_INCORRECT_GUESSES])
    display_health_bar(MAX_INCORRECT_GUESSES, MAX_INCORRECT_GUESSES)
    print(f"\n  {Style.BG_RED}{Style.WHITE}{Style.BOLD} ✖ GAME OVER! ✖ {Style.RESET}")
    print(f"  You ran out of guesses! The man has been hanged.")
    print(f"  The secret word was: {Style.CYAN}{Style.BOLD}{secret_word}{Style.RESET}")
    print(f"  Meaning: {Style.WHITE}{hint}{Style.RESET}\n")

    stats["losses"] += 1
    stats["streak"] = 0


# =============================================================================
# SESSION STATISTICS & REPLAY SYSTEM
# =============================================================================
def print_stats(stats):
    """Renders the player's lifetime session statistics in an aesthetic box."""
    total_games = stats["wins"] + stats["losses"]
    win_pct = (stats["wins"] / total_games * 100) if total_games > 0 else 0.0

    print(f"""
  {Style.CYAN}┌──────────────────────────────────────────────┐
  │              SESSION SCOREBOARD              │
  ├──────────────────────────────────────────────┤{Style.RESET}
  │  Total Games Played : {Style.BOLD}{total_games:<23}{Style.RESET}│
  │  Victories          : {Style.GREEN}{Style.BOLD}{stats['wins']:<23}{Style.RESET}│
  │  Defeats            : {Style.RED}{Style.BOLD}{stats['losses']:<23}{Style.RESET}│
  │  Win Rate           : {Style.YELLOW}{Style.BOLD}{win_pct:.1f}%{Style.RESET}{' ' * (22 - len(f'{win_pct:.1f}%'))}│
  │  Current Win Streak : {Style.MAGENTA}{Style.BOLD}{stats['streak']:<23}{Style.RESET}│
  {Style.CYAN}└──────────────────────────────────────────────┘{Style.RESET}
""")


def main():
    """Main program entry point handling session loop and replay selection."""
    stats = {
        "wins": 0,
        "losses": 0,
        "streak": 0
    }

    clear_screen()
    print_banner()
    print(f"""
  {Style.BOLD}Welcome to the Rich Text Hangman Game!{Style.RESET}
  
  {Style.CYAN}RULES & SPECIFICATIONS:{Style.RESET}
  • Secret word is chosen randomly from 5 predefined words.
  • You have a limit of {Style.BOLD}6 incorrect guesses{Style.RESET}.
  • Guess one alphabet letter at a time (A-Z).
  • Type {Style.YELLOW}'?'{Style.RESET} if you ever need a hint.
  • Duplicate guesses do not consume lives.
    """)
    input(f"  {Style.GREEN}Press [ENTER] to start your first round...{Style.RESET}")

    # Replay loop (while loop)
    while True:
        play_hangman(stats)
        print_stats(stats)

        # Prompt user to play again
        while True:
            choice = input(f"  {Style.CYAN}Would you like to play another round? (y/n): {Style.RESET}").strip().lower()
            if choice in ["y", "yes"]:
                break
            elif choice in ["n", "no", "exit", "quit"]:
                clear_screen()
                print_banner()
                print(f"  {Style.GREEN}Thank you for playing Hangman! See you next time!{Style.RESET}\n")
                print_stats(stats)
                sys.exit(0)
            else:
                print(f"  {Style.RED}Please type 'y' for yes or 'n' for no.{Style.RESET}")


if __name__ == "__main__":
    main()
