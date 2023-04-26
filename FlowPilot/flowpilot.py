import os
import re
import inspect
from inspect import isfunction
import json
from typing import Callable, Dict, List, Optional, Union, Any
from functools import wraps
import logging
from tqdm import tqdm
import pandas as pd
import textwrap


class CategoryRegister:
    def __init__(self, categories: List[str]):
        self.categories = categories
        
        self.functions: Dict[str, Dict[str, Optional[Callable]]] = {
            category: {} for category in categories
        }

    def is_valid_category(self, category_name: str) -> bool:
        """Check if the given category name is valid."""
        return category_name in self.categories

    def create_new_category(self, name: str) -> None:
        """Create a new category."""
        if name in self.categories:
            print(f"Category '{name}' already exists.")
        else:
            self.categories.append(name)
            self.functions[name] = {}

    
    def register_function(self, category: str, comment: Optional[str] = None) -> Callable:
        """Register a function in the specified category."""

        def decorator(func: Callable) -> Callable:
            func_name = func.__name__
            func.__category__ = category
            self.functions[category][func_name] = {
                'comment': comment,
                'function': func
            }
            return func

        return decorator
    
    def get_functions_by_category(self, category_name: str) -> Dict[str, Optional[str]]:
        return self.functions.get(category_name, {})


    def display_functions(self, category_name: Optional[str] = None, include_function: bool = False) -> None:
        """Display the functions registered in all or a specific category."""
        function_data: Dict[str, Union[str, Dict[str, List[Dict[str, str]]]]] = {
            "functions": {},
        }
        
        def format_function(func: Callable) -> str:
            lines = inspect.getsource(func).split('\n')
            dedented_lines = textwrap.dedent('\n'.join(lines)).split('\n')
            return CategoryRegister._remove_decorator('\n'.join(dedented_lines))

        if category_name is None:
            function_data["functions"] = {
                category: [
                    {
                        "name": func_name,
                        "comment": func_data['comment'] or "no comment",
                        "function definition": format_function(func_data['function']) if include_function else "Not Displayed"
                    }
                    for func_name, func_data in functions.items()
                ]
                for category, functions in self.functions.items()
                if functions
            }
        elif category_name in self.functions:
            function_data["functions"] = {
                category_name: [
                    {
                        "name": func_name,
                        "comment": func_data['comment'] or "no comment",
                        "function definition": format_function(func_data['function']) if include_function else "Not Displayed"
                    }
                    for func_name, func_data in self.functions[category_name].items()
                ],
            }
        else:
            print(f"Category '{category_name}' not found.")
            return

        print(json.dumps(function_data, indent=4, default=str))
        
    @staticmethod
    def _remove_decorator(func_str: str) -> str:
        """Remove the decorator from the function source code."""
        pattern = r"@\w+\.[a-z_]+\(.+?\)\n"
        match = re.search(pattern, func_str)
        if match:
            func_str = func_str[: match.start()] + func_str[match.end() :]
        return func_str
        
                
    def write_category_to_file(self, category_name: str, output_directory: str = ".") -> None:
        """Write functions in a specific category or all categories into a script file."""
        if category_name.lower() == "all":
            for category in self.functions:
                self._write_single_category_to_file(category, output_directory)
        else:
            self._write_single_category_to_file(category_name, output_directory)

    def _write_single_category_to_file(self, category_name: str, output_directory: str) -> None:
        if category_name not in self.functions:
            print(f"Category '{category_name}' not found.")
            return

        def format_function(func: Callable) -> str:
            lines = inspect.getsource(func).split('\n')
            dedented_lines = textwrap.dedent('\n'.join(lines)).split('\n')
            return CategoryRegister._remove_decorator('\n'.join(dedented_lines))

        file_name = f"{category_name}.py"
        output_path = os.path.join(output_directory, file_name)

        extractor = ImportExtractor()
        unique_imports = extractor.get_unique_imports(os.getcwd())

        with open(output_path, "w") as file:
            file.write("# This script was generated by FlowPilot\n")
            file.write("# Imports\n")
            # Write imports
            for import_line in unique_imports:
                file.write("try:\n")
                file.write(f"    {import_line}\n")
                file.write("except ImportError as e:\n")
                file.write(f"    print(f'Failed to import: {{e}}')\n")
            file.write("\n")

            # Write functions
            file.write("# Functions\n")
            for func_name, func_data in self.functions[category_name].items():
                file.write(format_function(func_data["function"]))
                file.write("\n\n")


    
    def search_functions(self, search_query: str, search_field: Optional[str] = None, case_sensitive: bool = False) -> List[Dict[str, str]]:
        """Search for functions based on name, category, or comment."""
        if search_field not in [None, "name", "category", "comment"]:
            raise ValueError("Invalid search_field. It should be one of 'name', 'category', or 'comment'.")

        if not case_sensitive:
            search_query = search_query.lower()

        def match(item: str) -> bool:
            if not case_sensitive:
                item = item.lower()
            return bool(re.search(search_query, item or ""))

        search_results = [
            {"name": func_name, "category": category, "comment": func_data['comment']}
            for category, functions in self.functions.items()
            for func_name, func_data in functions.items()
            if (
                (search_field is None and (match(func_name) or match(category) or match(func_data['comment'])))
                or (search_field == "name" and match(func_name))
                or (search_field == "category" and match(category))
                or (search_field == "comment" and match(func_data['comment']))
            )
        ]
        return search_results
    

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
    
    
    

class FlowPilot:
    def __init__(self, project_name: str):
        categories = ["data_reader", "data_transformer", "data_writer", "test"]
        self.project_name = project_name
        self.category_register = CategoryRegister(categories)
        self.project = Project(self.project_name)
        self._create_shortcuts_for_categories(categories)
    

    def _create_shortcuts_for_categories(self, categories: List[str]) -> None:
        """Create shortcuts for registering functions in categories."""
        for category in categories:
            setattr(self, category, lambda comment=None, cat=category: self.register_function(cat, comment))

    def create_new_category(self, name: str) -> None:
        """Create a new category and its shortcut."""
        self.category_register.create_new_category(name)
        self._create_shortcuts_for_categories([name])

    def register_function(self, category: str, comment: Optional[str] = None) -> Callable:
        """Register a function in a specific category."""
        return self.category_register.register_function(category, comment)

    def is_valid_category(self, category_name: str) -> bool:
        """Check if the category name is valid."""
        return self.category_register.is_valid_category(category_name)

    def custom(self, category_name: str, comment: Optional[str] = None) -> Callable:
        """Register a custom function in a category, creating the category if it does not exist."""
        if not self.category_register.is_valid_category(category_name):
            self.category_register.create_new_category(category_name)
        return self.category_register.register_function(category_name, comment)

    def display_functions(self, category_name: Optional[str] = None, include_function: bool = False) -> None:
        """Display the functions registered in all categories."""
        self.category_register.display_functions(category_name, include_function)

    
    def search_functions(self, search_query: str, search_field: Optional[str] = None) -> None:
        """Search for functions based on name, category, or comment."""
        search_results = self.category_register.search_functions(search_query, search_field)
        if search_results:
            print("Search results:")
            for result in search_results:
                print(f"Name: {result['name']}, Category: {result['category']}, Comment: {result['comment']}")
        else:
            print("No matching functions found.")
            
    def write_category_to_file(self, category_name: str, output_path: Optional[str] = None) -> None:
        """Write the functions of a specified category to a script file along with the necessary imports."""
        if output_path is None:
            output_path = self.project_name
        self.category_register.write_category_to_file(category_name, output_path)
            
            
class DataQualityConstraints:
    @staticmethod
    def expect_column_types(columns_types, expect_mode='expect_or_drop'):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                df = func(*args, **kwargs)
                for column, expected_type in columns_types.items():
                    if not pd.api.types.is_dtype_equal(df[column].dtype, expected_type):
                        if expect_mode == 'expect_or_drop':
                            mask = df[column].apply(lambda x: isinstance(x, expected_type))
                            df = df[mask]
                        elif expect_mode == 'expect_but_allow':
                            continue
                        elif expect_mode == 'expect_or_fail':
                            raise ValueError(f"Column '{column}' is not of expected type '{expected_type}'.")
                return df
            return wrapper
        return decorator
            
    
class Pipeline:
    def __init__(self, flow_pilot: FlowPilot):
        self.flow_pilot = flow_pilot
        self.steps = []

    def add_step(self, category: str, func: Callable, *args, **kwargs) -> None:
        self._validate_function_category(func, category)
        self.steps.append((func, args, kwargs))

    def _validate_function_category(self, func: Callable, category: str) -> None:
        """Validate that the function belongs to the specified category."""
        if not hasattr(func, "__category__"):
            raise ValueError(f"Function '{func.__name__}' is not registered in any category.")
        if func.__category__ != category:
            raise ValueError(f"Function '{func.__name__}' does not belong to category '{category}'.")

    def execute(self) -> Any:
        data = None
        for step, step_args, step_kwargs in self.steps:
            if data is None:
                data = step(*step_args, **step_kwargs)
            else:
                data = step(data, *step_args, **step_kwargs)
        return data
    
    def show_pipeline_steps(self) -> None:
        """Display the logical flow of the functions in the pipeline."""
        if not self.steps:
            print("The pipeline is empty.")
            return

        print("Pipeline steps:")
        for i, (step, step_args, step_kwargs) in enumerate(self.steps, start=1):
            step_category = step.__category__
            step_name = step.__name__
            step_args_str = ", ".join(map(str, step_args)) if step_args else ""
            step_kwargs_str = ", ".join(f"{k}={v}" for k, v in step_kwargs.items()) if step_kwargs else ""
            step_params_str = step_args_str + (", " if step_args_str and step_kwargs_str else "") + step_kwargs_str

            print(f"{i}. [{step_category}] {step_name}({step_params_str})")
            
    def get_pipeline_steps_json(self) -> str:
        
        """Return the pipeline steps as a JSON string."""
        steps_data = [
            {"name": step.__name__, "category": step.__category__}
            for step, _, _ in self.steps
        ]
        return json.dumps(steps_data)

    
class ImportExtractor:

    @staticmethod
    def extract_all_imports(file_content: str, ignore_nesting: bool = False) -> List[str]:
        base_regexes = [
            r'import [\w.]+ as [\w.]+',
            r'import [\w.]+',
            r'from [\w.]+ import [\w.]+ as [\w.]+',
            r'from [\w.]+ import [\w.]+',
        ]
        regexes = []

        if ignore_nesting:
            for regex in base_regexes:
                regexes.append(f'^{regex}')
                regexes.append(f'\n{regex}')
        else:
            regexes += base_regexes

        regex = re.compile(f'({"|".join(regexes)})')
        return [s.strip() for s in re.findall(regex, file_content)]

    @staticmethod
    def files_in_path(path: str) -> List[str]:
        files = []
        for r, d, f in os.walk(path):
            for file in f:
                files.append(os.path.join(r, file))
        return files

    @staticmethod
    def filter_file_list(file_list: List[str]) -> List[str]:
        return [item for item in file_list if ".git" not in item and "env" not in item]

    def get_import_list(self, file_list: List[str]) -> List[List[str]]:
        import_list = []
        for file_name in file_list:
            try:
                with open(file_name, mode='r') as f:
                    file_content = f.read()
                    import_list.append(self.extract_all_imports(file_content))
            except:
                pass

        return import_list

    @staticmethod
    def make_unique_list(import_list: List[List[str]]) -> List[str]:
        flat_list = [item for sublist in import_list for item in sublist]
        return list(set(flat_list))

    @staticmethod
    def clean_list(import_list: List[str]) -> List[str]:
        return [item for item in import_list if item != 'import .']

    def get_unique_imports(self, path: str) -> List[str]:
        files = self.filter_file_list(self.files_in_path(path))
        import_list = self.get_import_list(files)
        unique_imports = self.make_unique_list(import_list)
        return self.clean_list(unique_imports)
