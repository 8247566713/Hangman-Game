# 🎮 Rich Text-Based Hangman Game

> **CodeAlpha Python Programming Internship — Task 1**  
> An interactive, console-based Hangman game developed in pure Python, featuring rich terminal aesthetics, dynamic ASCII art gallows, live health tracking, letter bank indicators, hints, and session statistics.

---

## 🌟 Project Highlights

- **Pure Python, Zero External Dependencies**: Built entirely with Python's standard library (`sys`, `os`, `random`, `time`). Runs instantly on Windows, macOS, and Linux without needing `pip install`.
- **Rich Terminal UI**:
  - ✨ Full-color ANSI styling (vibrant cyan headers, green correct guesses, red mistake alerts, yellow hints).
  - 🪵 7-Stage detailed ASCII Gallows (from empty scaffold to final game-over stage).
  - 💚 Visual Health Bar (`[ ■ ■ ■ ■ ■ ■ ] (6/6)`) tracking remaining attempts.
  - 🔤 Interactive Letter Bank (`A-Z`) dynamically color-coded to show guessed, missed, and remaining letters.
  - 💡 Optional Clue/Hint System (Press `?` at any prompt).
  - 📊 Session Scoreboard tracking games played, wins, losses, win percentage, and current win streaks.
  - 🔁 Replay loop allowing back-to-back rounds without restarting the program.

---

## 🎯 Task Requirements & Scope Compliance

| Requirement | Implementation Details | Status |
| :--- | :--- | :---: |
| **5 Predefined Words** | Uses `WORD_COLLECTION` containing 5 curated words (`PYTHON`, `GALAXY`, `WIZARD`, `JUNGLE`, `SHADOW`) each with its category and educational hint. No external file or API needed. | ✅ Compliant |
| **Limit to 6 Incorrect Guesses** | `MAX_INCORRECT_GUESSES = 6`. Represents 6 stages of the hangman (Head, Torso, Left Arm, Right Arm, Left Leg, Right Leg). | ✅ Compliant |
| **Text-Based Console I/O** | All inputs and outputs run entirely within the terminal/command prompt. No graphics or audio libraries required. | ✅ Compliant |
| **Key Concepts Utilized** | • `random`: `random.choice()` for word selection.<br>• `while`: Main turn-based gameplay loop & replay loop.<br>• `if-else`: Input validation, win/loss evaluation, duplicate checking.<br>• `strings`: Slicing, `.upper()`, `.isalpha()`, `.join()`.<br>• `lists`: Word collections, guessed letters tracking, masked word display. | ✅ Compliant |

---

## 🕹️ Visual Gameplay Preview

```text
╔═══════════════════════════════════════════════════════════╗
║                  ★  H A N G M A N  ★                      ║
║            Classic Text-Based Word Guessing Game          ║
║               CodeAlpha Python Project Task-1             ║
╚═══════════════════════════════════════════════════════════╝

  Category: [Technology]   |   Word Length: 6 letters

       +---+
       |   |
       O   |
      /|\  |
           |
           |
    =========
    
  Lives Remaining: [ ■ ■ ■ ✖ ✖ ✖ ] (3/6)

  Current Word:  P Y T H _ _

  Letter Bank: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

  💡 Hint: A versatile programming language named after a British comedy troupe.

  Status: ✔ Good job! 'H' is in the word! (1 found)

  Enter a letter guess >> 
```

---

## 🚀 How to Run

### Prerequisites
- Python 3.7 or higher installed on your system.

### Running the Game
You can launch the game in any of the following easy ways:

1. **Double-Click (Easiest)**:
   - Double-click [`run.bat`](file:///c:/Users/my/OneDrive/Desktop/codealpha1/run.bat) in your folder.

2. **Using PowerShell**:
   ```powershell
   .\run.ps1
   ```

3. **Using Standard Python Command**:
   ```bash
   python hangman.py
   ```
   *(Or specify the direct Python path: `C:\Users\my\AppData\Local\Python\bin\python.exe hangman.py`)*

### Running Unit Tests
A test suite is included to verify core mechanics and scope adherence:
```bash
python test_hangman.py
```

---

## 📂 Project Structure

```
codealpha1/
│
├── hangman.py         # Main game application with rich UI and gameplay loops
├── test_hangman.py    # Unit test suite verifying game logic and scope constraints
└── README.md          # Project documentation, gameplay guide, and rubric compliance
```

---

## 🧠 Key Python Concepts Explained

### 1. `random` Module
```python
chosen_item = random.choice(WORD_COLLECTION)
secret_word = chosen_item["word"]
```
Selects a pseudo-random word object from the predefined collection each round.

### 2. `while` Loop
```python
while incorrect_guesses < MAX_INCORRECT_GUESSES:
    # Continuously accepts guesses and re-renders until win or max lives reached
```

### 3. `if-else` Conditions & Input Validation
```python
if len(user_input) != 1:
    # Reject strings with length != 1
elif not user_input.isalpha():
    # Reject digits and special characters
elif user_input in guessed_letters:
    # Reject already guessed letters without life penalty
elif user_input in secret_word:
    # Correct guess
else:
    # Incorrect guess - deducts 1 life
```

### 4. Strings & Lists
- Strings are manipulated using `.strip()`, `.upper()`, `.isalpha()`, `.count()`, and formatted f-strings.
- Lists are used for:
  - `WORD_COLLECTION`: list of dictionaries containing word details.
  - `guessed_letters`: dynamic list recording player attempts.
  - `HANGMAN_STAGES`: indexed list of 7 ASCII art gallows states.
