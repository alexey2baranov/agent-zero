import json
import os

# Get the path to the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

# State file stored in the same directory as the script
STORAGE_FILE = os.path.join(SCRIPT_DIR, "state.json")

def load_state():
    """
    Loads the current script state from the JSON storage file.
    Returns a dictionary containing the stored state.
    """
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_state(state):
    """
    Saves the given state dictionary to the JSON storage file.
    """
    with open(STORAGE_FILE, 'w') as file:
        json.dump(state, file, indent=4)
