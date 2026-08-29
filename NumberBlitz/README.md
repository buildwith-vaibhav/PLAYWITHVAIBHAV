# Number Blitz

A simple and fun command-line number guessing game written in Python. The computer picks a secret number between 1 and 100, and you have 7 chances to guess it correctly.

## Features

- Personalized greeting with the player's name
- Random number generation between 1 and 100
- 7 attempts to guess the correct number
- Helpful hints ("higher" or "lower") after every wrong guess
- Remaining chances counter
- Option to play multiple rounds
- Input validation (rejects numbers outside 1–100 without counting as an attempt)

## Requirements

- Python 3.6 or higher
- No external libraries required (uses only Python standard library)

## How to Run

1. Clone the repository or download the file

2. Run the game:
   ```bash
   python Number_Blitz.py
   ```

3. Enter your name and follow the on-screen instructions.

## How to Play

1. Enter your name when prompted.
2. Type `y` to start the game.
3. Guess a number between **1 and 100**.
4. After each guess, the game will tell you if the secret number is **higher** or **lower**.
5. You have a maximum of **7 attempts**.
6. After the game ends, you can choose to play again.

### Example Gameplay

```
Enter Your Name: Alex
-----------Welcome to the number guessing game----------
Rules
1.You have to guess a number between 1 to 100
2.if the number you choose is also chosen by the computer you win
3.if the number is incorrect the computer will tell you that the chosen number is higher or lower than your number
4.You will get 7 chances to guess the number 
5.If you failed to guess the number in given chances you will lose
start the game(y/n)y
-----------All the best-----------
----------- Enjoy the game----------
Enter Your Number: 50
wrong entry the no. is higher than 50
You have 6 chances left
Enter Your Number: 75
wrong entry the no. is lower than 75
You have 5 chances left
...
----------- Alex won the game---------
```

## Project Structure

```
.
├── Number_Blitz.py   # Main game file
└── README.md
```

## Rules Summary

| Rule                  | Details                          |
|-----------------------|----------------------------------|
| Number Range          | 1 to 100                         |
| Maximum Attempts      | 7                                |
| Hints                 | Higher / Lower                   |
| Replay                | Yes (after each game)            |
| Invalid Input         | Numbers outside 1–100 are ignored|

## Notes

- The game continues until you choose not to play again (`n` / `N`).
- Entering a number outside the range 1–100 does **not** reduce your remaining attempts.
- The secret number is generated randomly every new game.
