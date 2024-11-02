import subprocess
import pytest
from python.aci import storage
from python.aci.constants import WINDOW, OVERLAP

@pytest.fixture
def clear_state():
    """
    Clears the state before running each test.
    """
    storage.save_state({})

@pytest.fixture
def test_file(tmpdir):
    """
    Create a temporary test file with WINDOW * 10 lines.
    This ensures the file is large enough even if WINDOW is set to a large value.
    """
    test_file_path = tmpdir.join("testfile.txt")
    lines = "\n".join([f"Line {i+1}" for i in range(WINDOW * 10)])  # Create WINDOW * 10 lines
    test_file_path.write(lines)
    return str(test_file_path)

@pytest.fixture
def setup_open_command(test_file, clear_state):
    """
    Setup by running the open.py script to open the test file at line 50.
    This prepares the state for testing scroll_up.py.
    """
    subprocess.run(
        ["python3", "python/aci/open.py", test_file, str(WINDOW * 5)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return test_file

def test_scroll_up_command(setup_open_command):
    """
    Test the scroll_up.py command after running open.py.
    """
    # Run the scroll_up.py script as a subprocess
    result = subprocess.run(
        ["python3", "python/aci/scroll_up.py"],
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

    # Calculate the expected line after scrolling up
    expected_line = WINDOW * 4 + OVERLAP

    # Check if the correct lines after scrolling up are printed
    assert f"Line {expected_line}" in output  # Since it should scroll up from line 50 by WINDOW - OVERLAP

    # Check if the state was updated correctly after scrolling
    state = storage.load_state()
    assert state.get('CURRENT_LINE') == expected_line  # The new line number should reflect the scrolled-up position
