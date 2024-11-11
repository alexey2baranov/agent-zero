#!/usr/bin/env python3

import os
import argparse
from open import open_file

def create():
    """
    Creates a new file with the given name and opens it. 
    If the file already exists, it opens the existing file.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Create and open a new file with the specified name.")
    parser.add_argument("filename", type=str, help="The name of the file to create and open.")
    args = parser.parse_args()

    # Check if `file` is an absolute path, but not relative
    if not os.path.isabs(args.filename):
        print(f"Error: Please use absolute paths for `path` arg {args.filename}'")
    # Check if the file already exists
    elif os.path.exists(args.filename):
        print(f"Error: File '{args.filename}' already exists.")
        open_file(args.filename)  # Open the existing file if it exists
    # Check if the file folder exists
    elif not os.path.exists(os.path.dirname(args.filename)):
        print(f"Error: The folder '{os.path.dirname(args.filename)}' does not exist.")
    # Create the new file
    else:
        with open(args.filename, 'w') as new_file:
            new_file.write("\n")  # Add an empty newline, similar to the original script behavior
        print(f"File '{args.filename}' created.")
        
        # Open the newly created file
        open_file(args.filename)

if __name__ == "__main__":
    create()
