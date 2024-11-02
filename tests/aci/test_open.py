import subprocess
import os
import pytest
from python.aci import storage
from python.aci.constants import WINDOW

@pytest.fixture
def test_file(tmpdir):
    """
    Create a temporary test file with some lines.
    """
    test_file_path = tmpdir.join("testfile.txt")
    lines = "\n".join([f"Line {i+1}" for i in range(1000)])
    test_file_path.write(lines)
    return str(test_file_path)

def test_open_command(test_file):
    """
    Test the open.py command by running it and checking the output.
    """
    # Run the open.py script as a subprocess
    result = subprocess.run(
        ["python3", "python/aci/open.py", test_file, "10"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Extract the output
    output = result.stdout
    error = result.stderr

    # Assert no errors
    assert result.returncode == 0
    assert "File not found" not in error

    # Check if the correct lines are printed
    assert "Line 10" in output
    assert "Line 15" in output  # WINDOW size, so expect +/- lines

    # Check if state was saved correctly
    state = storage.load_state()
    assert state.get('CURRENT_FILE') == os.path.realpath(test_file)
    assert state.get('CURRENT_LINE') == WINDOW // 2
