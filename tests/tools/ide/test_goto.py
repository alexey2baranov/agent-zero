import subprocess
import os
import pytest
from python.tools.aci import storage
from python.tools.aci.constants import WINDOW

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
    lines = "\n".join([f"Line {i+1}" for i in range(WINDOW * 10)])  # Create WINDOW * 10 lines
    test_file_path.write(lines)
    return str(test_file_path)

@pytest.fixture
def setup_open_command(test_file, clear_state):
    """
    Setup by running the open.py script to open the test file at line 10.
    This prepares the state for testing goto.py.
    """
    subprocess.run(
        ["python3", "python/tools/aci/open.py", test_file, str(WINDOW // 2)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return test_file

def test_goto_command(setup_open_command):
    """
    Test the goto.py command after opening the test file.
    """
    # Run the goto.py script as a subprocess to go to line 50
    result = subprocess.run(
        ["python3", "python/tools/aci/goto.py", "500"],
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
    assert "Error" not in error

    # Check if the correct lines are printed
    assert "Line 500" in output

    # Check if state was updated correctly after going to line 50
    state = storage.load_state()
    assert state.get('CURRENT_LINE') == max(1, 500 + WINDOW // 2 - WINDOW // 6)

