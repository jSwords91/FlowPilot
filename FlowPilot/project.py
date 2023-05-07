import os
import re
import inspect
from typing import Callable, Dict, List, Optional, Union, Any


from category import *

class Project:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self._create_project_directory()

    def _create_project_directory(self) -> None:
        """Create the project directory."""
        if not os.path.exists(self.project_name):
            os.makedirs(self.project_name)
            
    def _generate_function_docstring(self, func: Callable, comment: Optional[str] = None) -> str:
        signature = inspect.signature(func)
        input_types = {
            key: param.annotation
            for key, param in signature.parameters.items()
            if param.annotation != inspect.Parameter.empty
        }
        output_type = (
            signature.return_annotation
            if signature.return_annotation != inspect.Signature.empty
            else "Any"
        )
        indent = " " * 4

        docstring_lines = [
            f"{comment or 'No description'}",
            "",
            "Input types:",
            *[f"{indent}{key}: {value}" for key, value in input_types.items()],
            "",
            f"Output type: {output_type}",
        ]
        indented_docstring = "\n".join([indent + line for line in docstring_lines])

        return indented_docstring

    @staticmethod
    def _remove_decorator(func_str: str) -> str:
        """Remove the decorator from the function source code."""
        pattern = r"@\w+\.[a-z_]+\(.+?\)\n"
        match = re.search(pattern, func_str)
        if match:
            func_str = func_str[: match.start()] + func_str[match.end() :]
        return func_str
    