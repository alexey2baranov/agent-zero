import os
import inspect
import ast
from unittest.mock import Mock
from python.tools.memory_tool import save


from python.helpers.tool import Tool

class RememberCode(Tool):
    """
    Tool to summarize code in a file and store the summaries in a vector database.
    """

    def __init__(self, agent, name, args, message, **kwargs):
        super().__init__(agent, name, args, message, **kwargs)

    def summarize_file(self, file_path):
        """
        Summarize the code in the given file.
        """
        with open(file_path, 'r') as file:
            code = file.read()

        # Parse the code to identify classes, methods, and functions
        # Generate summaries for the entire file, each class, and each function
        # Store the summaries in a structured format
        summary = self._generate_summary(code)
        return summary

    def _generate_summary(self, code):
        """
        Generate a summary for the given code.
        """
        # Implement the logic to parse the code and generate summaries
        tree = ast.parse(code)
        summaries = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                summaries[node.name] = self._summarize_class(node)
            elif isinstance(node, ast.FunctionDef):
                summaries[node.name] = self._summarize_function(node)
        return summaries

    def _summarize_class(self, class_node):
        """
        Generate a summary for the given class.
        """
        summary = {
            'name': class_node.name,
            'methods': {}
        }
        expected_summary = {'name': class_node.name, 'methods': {}}
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef):
                summary['methods'][node.name] = self._summarize_function(node)
        return summary
    def _summarize_function(self, function_node):
        """
        Generate a summary for the given function.
        """
        summary = {
            'name': function_node.name,
            'args': [arg.arg for arg in function_node.args.args],
            'docstring': ast.get_docstring(function_node) or 'No docstring available'
        }
        return summary

    def _store_summary(self, summary):
        """
        Store the generated summary in the vector database.
        """
        save(agent=self.agent, text=str(summary))
    def execute(self, file_path, **kwargs):
        return self.summarize_file(file_path)
