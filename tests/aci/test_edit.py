import subprocess
import os
import pytest
from python.aci import storage
from python.aci.constants import WINDOW

@pytest.fixture
def clear_state():
    """
    Fixture to clear the current state before each test.
    """
    storage.save_state({})

@pytest.fixture
def test_file(tmpdir):
    """
    Create a temporary test file with WINDOW * 2 lines.
    This ensures the file is large enough to test the edit functionality.
    """
    test_file_path = tmpdir.join("testfile.py")
    lines = "\n".join([f"line{i+1} = {i+1}" for i in range(WINDOW * 10)])  # Create WINDOW * 10 lines
    test_file_path.write(lines)
    return str(test_file_path)

@pytest.fixture
def setup_open_command(test_file, clear_state):
    """
    Set up the state by running the open.py script to open the test file.
    This prepares the state for testing edit.py.
    """
    subprocess.run(
        ["python3", "python/aci/open.py", test_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return test_file

def test_edit_command_no_lint_errors(setup_open_command):
    """
    Test the edit.py command for a file that doesn't introduce any linting errors.
    """
    # Edit the test file at lines 10-15 and replace with "Edited Line"
    result = subprocess.run(
        ["python3", "python/aci/edit_linting.py", "10", "15", """def some_function():
    print('Edited Line')
    print('Edited Line')
    print('Edited Line')
    print('Edited Line')
    print('Edited Line')
    print('Edited Line')
    print('Edited Line')
    print('Edited Line')
    print('Edited Line')
    print('Edited Line')"""],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Extract the output
    output = result.stdout
    error = result.stderr

    # Assert no errors
    assert result.returncode == 0
    assert "ERRORS:" not in output
    assert "Your changes have NOT been applied" not in output

    # Check if the correct lines have been updated in the file
    with open(setup_open_command, 'r') as file:
        lines = file.readlines()
        for i in range(11, 20):  # Python is zero-indexed, so lines 10-15 are 9-14 in the list
            assert lines[i] == "    print('Edited Line')\n"

    # Check if the state was updated correctly
    state = storage.load_state()
    assert state.get('CURRENT_LINE') == (10 // 2) + 9 + 1  # The middle of the edited region

def test_edit_command_with_lint_errors(setup_open_command):
    """
    Test the edit.py command for a file that introduces linting errors.
    """
    # Edit the test file at lines 10-15 and replace with invalid Python code
    result = subprocess.run(
        ["python3", "python/aci/edit_linting.py", "100", "115", "def invalid_code(:\n"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Extract the output
    output = result.stdout
    error = result.stderr

    # Assert errors were detected
    assert result.returncode == 0
    assert "ERRORS:" in output
    assert "Your changes have NOT been applied" in output

    # Check that the original content was restored (i.e., the edit was not applied)
    with open(setup_open_command, 'r') as file:
        lines = file.readlines()
        for i in range(100, 115):  # Check the original content is still present
            assert lines[i].startswith("line")

    # Check if the state was restored correctly after linting errors
    state = storage.load_state()
    assert state.get('CURRENT_LINE') == 108  # Should revert to the original current line
