import subprocess
import os
import pytest


@pytest.fixture
def test_file(tmpdir):
    return str(tmpdir.join("testfile.txt"))

@pytest.fixture
def non_existent_dir(tmpdir):
    return str(tmpdir.join("non_existent_dir/testfile.txt"))
def test_create_relative_path():
    # Run the create.py script with a relative path
    result = subprocess.run(
        ["python3", "python/aci/create.py", "relative/path/testfile.txt"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Extract the output
    output = result.stdout
    error = result.stderr

    # Assert no errors in execution
    assert result.returncode == 0
    
    # Check that the appropriate error message is displayed
    assert "Error: Please use absolute paths for `create` arg'relative/path/testfile.txt'" in output

def test_create_new_file(test_file):
    # Run the create.py script as a subprocess
    result = subprocess.run(
        ["python3", "python/aci/create.py", test_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )


    # Extract the output
    output = result.stdout
    error = result.stderr

    # Assert no errors
    assert result.returncode == 0
    assert "Error" not in error

    # Check if the file was created
    assert os.path.exists(test_file)
    assert "File '{}' created.".format(test_file) in output

def test_create_existing_file(test_file):
    """
    Test attempting to create a file that already exists.
    """
    # Create the file first
    with open(test_file, 'w') as f:
        f.write("Existing content")

    # Run the create.py script as a subprocess
    result = subprocess.run(
        ["python3", "python/aci/create.py", test_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Extract the output
    output = result.stdout
    error = result.stderr

    # Assert no errors
    assert result.returncode == 0
    assert "Error: File '{}' already exists.".format(test_file) in output

def test_create_in_non_existent_directory(non_existent_dir):
    """
    Test attempting to create a file in a non-existent directory.
    """
    # Run the create.py script as a subprocess
    result = subprocess.run(
        ["python3", "python/aci/create.py", non_existent_dir],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Extract the output
    output = result.stdout
    error = result.stderr

    # Assert no errors
    assert result.returncode == 0
    assert "Error: The folder '{}' does not exist.".format(os.path.dirname(non_existent_dir)) in output
