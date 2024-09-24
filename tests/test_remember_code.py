import pytest
from python.tools.remember_code import RememberCode
from unittest.mock import Mock
@pytest.fixture
def sample_code_file(tmp_path):
    code = """
class SampleClass:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f'Hello, {self.name}!'

def sample_function(a, b):
    return a + b
"""
    file_path = tmp_path / 'sample_code.py'
    file_path.write_text(code)
    return file_path

def test_remember_code(sample_code_file):
    mock_agent = Mock()
    mock_agent.config.memory_subdir = 'test_memory'
    mock_agent.config.embeddings_model = Mock()
    mock_agent.config.embeddings_model.model = 'test_model'
    mock_agent.config.embeddings_model.embed_documents = Mock(return_value=[[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])
    remember_code = RememberCode(agent=mock_agent, name='remember_code', args={}, message='')
    summary = remember_code.summarize_file(str(sample_code_file))
    expected_summary = {
        'SampleClass': {
            'name': 'SampleClass',
            'methods': {
                '__init__': {
                    'name': '__init__',
                    'args': ['self', 'name'],
                    'docstring': 'No docstring available'
                },
                'greet': {
                    'name': 'greet',
                    'args': ['self'],
                    'docstring': 'No docstring available'
                }
            }
        },
        'sample_function': {
            'name': 'sample_function',
            'args': ['a', 'b'],
            'docstring': 'No docstring available'
        }
    }
    assert summary == expected_summary
