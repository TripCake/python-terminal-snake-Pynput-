# python-terminal-snake-Pynput

An ASCII terminal-based snake game. Programmed in Python.

This code uses ANSI escape codes to reposition the cursor and efficiently change the game state only as needed. It also utilizes `sys.stdout.write(s)` with flushing instead of the standard Python `print()`. This makes the game extremely fast. 

In the repository, there are four files:
- One that uses the `pynput` library to register key inputs and is cross-platform as long as you have the `pynput` dependency.
- One that uses `sys.stdin.read()` combined with `select.select()` to be compatible with Linux or Darwin.
- One that uses `msvcrt` from the Microsoft C standard library to be compatible with Windows.
- The fourth file is an optional init file that will run the appropriate file depending on your operating system.

## Features
- Extremely fast
- No required dependencies
- A good opprotunity to learn about ANSI escape codes

### Optional Dependency: `pynput`
This project has an optional dependency on `pynput`. If you need additional functionality requiring `pynput`, install it separately:
```sh
pip install pynput
```

## Usage
To play the game, run the init.py script in your favourite terminal with python.
```sh
python init.py
```
