#!/usr/bin/env python3

import os
import argparse
import storage
from helpers import _constrain_line, _print
from constants import WINDOW

def open_file():
    """
    Opens the file and optionally navigates to a specific line. Stores the file and line in the state.
    """
    parser = argparse.ArgumentParser(description="Open a file and display content with optional line navigation.")
    parser.add_argument("file", help="The path to the file to open")
    parser.add_argument("line_number", type=int, nargs="?", default=None, help="The line number to start from (optional)")
    args = parser.parse_args()

    # Check if the file exists
    if not os.path.exists(args.file):
        print(f"File {args.file} not found")
        return

    # Handle if a directory is passed instead of a file
    if os.path.isdir(args.file):
        print(f"Error: {args.file} is a directory. You can only open files.")
        return
    
    state= storage.load_state()
    window= state.get("WINDOW", WINDOW)


    # Determine the starting line
    if args.line_number is None:
        # Default to the middle of the window if no line number is provided
        line_number = window // 2
    else:
        line_number = args.line_number

    # Store CURRENT_FILE and CURRENT_LINE in the state
    state = {
        "CURRENT_FILE": os.path.realpath(args.file),
        "CURRENT_LINE": line_number
    }
    storage.save_state(state)

    # Call constrain and print functions to display the file contents
    _constrain_line()  # This updates CURRENT_LINE if needed and stores the updated value
    _print()           # This prints the file content window

if __name__ == "__main__":
    open_file()
