import os
from constants import WINDOW
import storage

def _constrain_line():
    """
    Constrains the current line number based on the total number of lines in the current file and the window size.
    Fetches `CURRENT_FILE` and `CURRENT_LINE` from the state, adjusts the line number if needed, and stores the updated
    line number back into the state.
    
    Returns:
        int: The constrained line number.
    """
    # Load the current state
    state = storage.load_state()

    # Get the current file and line from the state
    current_file = state.get('CURRENT_FILE')
    current_line = state.get('CURRENT_LINE', 1)
    window= state.get('WINDOW', WINDOW)

    # Check if the file is open or exists
    if not current_file or not os.path.isfile(current_file):
        print("No file open. Use the 'open' command first.")
        return current_line  # Returning the current line if no file is found

    # Calculate the total number of lines in the file
    with open(current_file, 'r') as file:
        total_lines = len(file.readlines())

    # Constrain the current line based on the window size
    half_window = window // 2
    current_line = max(half_window, current_line)
    current_line = min(current_line, total_lines)

    # Store the updated CURRENT_LINE back into the state
    state['CURRENT_LINE'] = current_line
    storage.save_state(state)

    return current_line



def _print():
    """
    Prints the file content with context around the current line from the state.
    This simulates the window of lines displayed around the current line.
    """
    # Load state for the current file and line
    state = storage.load_state()
    current_file = state.get('CURRENT_FILE')
    current_line = state.get('CURRENT_LINE', 1)
    window= state.get('WINDOW', WINDOW)


    if not current_file or not os.path.isfile(current_file):
        print("No file open.")
        return

    # Open the file and read the lines
    with open(current_file, 'r') as file:
        lines = file.readlines()

    total_lines = len(lines)
    real_path = os.path.realpath(current_file)
    print(f"[File: {real_path} ({total_lines} lines total)]")

    # Calculate how many lines are above and below
    lines_above = max(0, current_line - window // 2)
    lines_below = max(0, total_lines - current_line - window // 2)

    if lines_above > 0:
        print(f"({lines_above} more lines above)")
    
    # Print lines within the window range
    start_line = max(0, current_line - window // 2)
    end_line = min(total_lines, current_line + window // 2)

    for i in range(start_line, end_line):
        print(f"{i+1}: {lines[i].rstrip()}")

    if lines_below > 0:
        print(f"({lines_below} more lines below)")
