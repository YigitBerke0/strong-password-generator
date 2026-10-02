# Strong Password Generator

A robust, terminal-based password generator written in Python. This tool generates secure passwords, calculates their cryptographic strength, and allows you to securely save your chosen credentials locally.

## Features

- **Customizable Difficulty:** Choose between 3 levels of complexity (Easy: Letters only, Medium: Letters + Digits, Hard: Letters + Digits + Symbols).
- **Multiple Options:** Generates 3 distinct password combinations based on your criteria, allowing you to choose the one you prefer.
- **Strength Analysis:** Calculates the estimated brute-force cracking time (assuming a modern cracking speed of 10 billion guesses per second) based on the password's length and character pool size.
- **Local Storage:** Prompts you to label your chosen password (e.g., "Steam Account") and appends it to a local `passwords.txt` file.
- **Secure by Design:** The `passwords.txt` file is explicitly ignored via `.gitignore` to ensure your sensitive data is never accidentally pushed to a public repository.
