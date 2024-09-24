import pytest
from python.tools.memory_tool import Memory

@pytest.fixture
def setup_memory_tool():
    memory_tool = Memory()
    return memory_tool

def test_search(setup_memory_tool):
    memory_tool = setup_memory_tool
    result = memory_tool.execute(query="test query")
    assert isinstance(result, str)

def test_save(setup_memory_tool):
    memory_tool = setup_memory_tool
    result = memory_tool.execute(memorize="test memory")
    assert isinstance(result, str)

def test_delete(setup_memory_tool):
    memory_tool = setup_memory_tool
    result = memory_tool.execute(delete="test id")
    assert isinstance(result, str)

def test_forget(setup_memory_tool):
    memory_tool = setup_memory_tool
    result = memory_tool.execute(forget="test query")
    assert isinstance(result, str)
