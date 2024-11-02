#!/usr/bin/env python3

import os
import argparse
from helpers import _constrain_line, _print
import storage
from constants import WINDOW

def goto():
    """
    Moves the window to show a specific line number in the currently open file.
    """
    # Parse the command line arguments to get the target line number
    parser = argparse.ArgumentParser(description="Move to a specific line number in the file.")
    parser.add_argument("line_number", type=int, help="The line number to move to")
    args = parser.parse_args()

    # Load the current state
    state = storage.load_state()
    current_file = state.get('CURRENT_FILE')
    current_line = int(state.get('CURRENT_LINE', 1))
    window= state.get("WINDOW", WINDOW)


    # Check if a file is open
    if not current_file or not os.path.isfile(current_file):
        print("No file open. Use the 'open' command first.")
        return

    # Get the total number of lines in the file
    with open(current_file, 'r') as file:
        lines = file.readlines()
        total_lines = len(lines)

    # Check if the provided line number is valid
    if args.line_number < 1 or args.line_number > total_lines:
        print(f"Error: <line> must be between 1 and {total_lines}")
        return

    # Calculate the target line to display in the middle of the window
    offset = window // 6
    target_line = max(1, args.line_number + window // 2 - offset)

    # Update the state with the new CURRENT_LINE
    state['CURRENT_LINE'] = target_line
    storage.save_state(state)

    # Constrain the line and print the updated window
    _constrain_line()
    _print()

if __name__ == "__main__":
    goto()
