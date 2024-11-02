import subprocess
import os
import pytest
from python.aci import storage
from python.aci.constants import WINDOW, OVERLAP

@pytest.fixture
def clear_state():
    storage.save_state({})

@pytest.fixture
def test_file(tmpdir):
    """
    Create a temporary test file with WINDOW * 2 lines.
    This ensures the file is large enough even if WINDOW is set to a large value.
    """
    test_file_path = tmpdir.join("testfile.txt")
    lines = "\n".join([f"Line {i+1}" for i in range(WINDOW * 10)])  # Create WINDOW * 2 lines
    test_file_path.write(lines)
    return str(test_file_path)

@pytest.fixture
def setup_open_command(test_file, clear_state):
    """
    Setup by running the open.py script to open the test file at line 10.
    This prepares the state for testing scroll_down.py.
    """
    subprocess.run(
        ["python3", "python/aci/open.py", test_file, str(WINDOW)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return test_file

def test_scroll_down_command(setup_open_command):
    """
    Test the scroll_down.py command after running open.py.
    """
    # Run the scroll_down.py script as a subprocess
    result = subprocess.run(
        ["python3", "python/aci/scroll_down.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Extract the output
    output = result.stdout
    error = result.stderr

    # Assert no errors
    assert result.returncode == 0
    assert "No file open" not in output
    assert "File not found" not in error

    # Calculate the expected line after scrolling down
    expected_line = WINDOW + (WINDOW - OVERLAP)

    # Check if the correct lines after scrolling down are printed
    assert f"Line {expected_line}" in output  # Since it should scroll down from line 10 by WINDOW - OVERLAP

    # Check if the state was updated correctly after scrolling
    state = storage.load_state()
    assert state.get('CURRENT_LINE') == expected_line  # The new line number should reflect the scrolled-down position
