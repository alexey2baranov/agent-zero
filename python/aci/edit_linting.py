#!/usr/bin/env python3

import os
import argparse
import subprocess

from pyparsing import line
from helpers import _print, _constrain_line
import storage
from constants import WINDOW  # Import the WINDOW constant

def run_linter(file_path):
    """
    Runs the linter on the given file and returns the output.
    """
    linter_cmd = ["flake8", "--isolated", "--select=F821,F822,F831,E111,E112,E113,E999,E902", file_path]
    result = subprocess.run(linter_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout

def call_split_string(lint_output, linter_before_edit, start_line, end_line, line_count):
    """
    Calls _split_string.py as a subprocess to filter linting errors based on the affected lines.
    """

    cmd = ["python3", os.path.join(os.path.dirname(os.path.realpath(__file__)), "_split_string.py"), lint_output, linter_before_edit, str(start_line), str(end_line), str(line_count)]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout

def edit():
    """
    Edits the lines between <start_line> and <end_line> with the new content provided.
    If the file is a Python file, it runs linting checks after the edit.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Edit lines in a file with new content.")
    parser.add_argument("start_line", type=int, help="The starting line number to edit.")
    parser.add_argument("end_line", type=int, help="The ending line number to edit.")
    parser.add_argument("replace_to", type=str, help="The replacement content for the specified lines. Use \\n for multiline content.")
    args = parser.parse_args()

    # Load the current state
    state = storage.load_state()
    current_file = state.get('CURRENT_FILE')
    current_line = int(state.get('CURRENT_LINE', 1))

    # Check if a file is open
    if not current_file or not os.path.isfile(current_file):
        print("No file open. Use the 'open' command first.")
        return

    # Read the current file content
    with open(current_file, 'r') as file:
        lines = file.readlines()

    # Validate the line range
    start_line = args.start_line - 1  # Adjust for 0-indexing
    end_line = args.end_line - 1      # Adjust for 0-indexing (Python slices exclude end)

    if start_line < 0 or end_line > len(lines):
        print(f"Line range {args.start_line}:{args.end_line} is out of bounds for the file.")
        return
    elif start_line== len(lines) and end_line== len(lines):
        lines.append("")
    

    # Backup the current file in /root/ with the basename and _backup appended
    backup_file = os.path.join("~", f"{os.path.basename(current_file)}_backup")
    backup_file = os.path.expanduser(backup_file)  # Expand the '~' to the full home directory path
    with open(backup_file, 'w') as backup:
        backup.writelines(lines)

    # Determine if the file is a Python file and run lint checks only if it is
    linter_before_edit = run_linter(current_file) if current_file.endswith('.py') else ""

    line_count = args.replace_to.count('\n') + 1  # Count the number of lines in the replacement content
    # Replace the content of the specified lines (inclusive)
    lines[start_line:end_line + 1] = [args.replace_to + "\n"]  # +1 to include the end_line


    # Write the updated content back to the file
    with open(current_file, 'w') as file:
        file.writelines(lines)

    if current_file.endswith('.py'):
        linter_after_edit = run_linter(current_file)        # Lint the file after applying changes
        # Call _split_string.py to filter the lint output
        lint_output = call_split_string(linter_after_edit, linter_before_edit, start_line + 1, end_line + 1, line_count)
    else:
        lint_output = ""  # Set lint_output to an empty string for non-Python files

    if not lint_output.strip():
        # Update the current line and print the result
        state['CURRENT_LINE'] = line_count // 2 + start_line + 1  # Adjust back to 1-indexed when updating CURRENT_LINE
        state['WINDOW'] = line_count+10
        storage.save_state(state)
        _constrain_line()
        _print()  # Use the default window size

        # Inform the user that the file was updated successfully
        print("File updated. Please review the changes and make sure they are correct (correct indentation, no duplicate lines, etc).")

    # If there are any linting errors, restore the backup
    else:
        # Print linting error message at the beginning
        print("Your proposed edit has introduced new syntax error(s). Please read this error message carefully and retry editing.")
        print("")
        print("ERRORS:")
        print(lint_output)
        print("")

        # Print preview of the edit
        print("This is how your edit would have looked if applied")
        print("-------------------------------------------------")
        
        # Update CURRENT_LINE to reflect the center of the edited lines for preview
        state['CURRENT_LINE'] = (line_count // 2) + start_line + 1
        state['WINDOW'] = line_count+10

        storage.save_state(state)

        # Show the result of the failed edit (pass custom window for preview)
        _constrain_line()  # Ensure the line number is within the correct bounds
        _print()  # Pass the custom window size for the preview

        print("-------------------------------------------------")

        # Restore the original content from the backup
        with open(backup_file, 'r') as backup:
            original_lines = backup.readlines()
        with open(current_file, 'w') as file:
            file.writelines(original_lines)

        # Print the original content with adjusted window size
        state['CURRENT_LINE'] = (end_line - start_line + 1) // 2 + start_line + 1  # Set to center of original content
        state['WINDOW'] = end_line - start_line + 10
        storage.save_state(state)

        print("This is the original code before your edit")
        print("-------------------------------------------------")
        
        _constrain_line()  # Show the original content after restoring from backup
        _print()  # Pass the custom window size to show the original content

        print("-------------------------------------------------")

        # Final message to instruct the user
        print("Your changes have NOT been applied. Please fix your edit command and try again.")
        print("You either need to 1) Specify the correct start/end line arguments or 2) Correct your edit code.")
        print("DO NOT re-run the same failed edit command. Running it again will lead to the same error.")
    
    # remove backup file
    os.remove(backup_file)

    state['WINDOW'] = WINDOW
    storage.save_state(state)
if __name__ == "__main__":
    edit()
