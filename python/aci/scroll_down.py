#!/usr/bin/env python3

import os
from helpers import _constrain_line, _print
from constants import WINDOW, OVERLAP
import storage

def scroll_down():
    """
    Scrolls down the current file by the number of lines specified by the WINDOW constant.
    Adjusts the CURRENT_LINE in the state and prints the updated window of lines.
    """
    # Load the current state
    state = storage.load_state()
    current_file = state.get('CURRENT_FILE')
    current_line = state.get('CURRENT_LINE', 1)
    window= state.get("WINDOW", WINDOW)

    # Check if a file is open
    if not current_file or not os.path.isfile(current_file):
        print("No file open. Use the 'open' command first.")
        return

    # Update CURRENT_LINE after constraining it within bounds
    state['CURRENT_LINE'] += window - OVERLAP
    
    # Save the updated CURRENT_LINE
    storage.save_state(state)

    _constrain_line()
    # Print the updated file window
    _print()

if __name__ == "__main__":
    scroll_down()
