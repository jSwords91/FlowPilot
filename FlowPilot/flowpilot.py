from typing import Callable, Dict, List, Optional, Union, Any
from functools import wraps

from category import *
from project import *
from pipes import *
from import_extractor import *

class FlowPilot:
    def __init__(self, project_name: str):
        categories = ["data_reader", "data_transformer", "data_writer", "test"]
        self.project_name = project_name
        self.category_register = CategoryRegister(categories)
        self.project = Project(self.project_name)
        self._create_shortcuts_for_categories(categories)


    def _create_shortcuts_for_categories(self, categories: List[str]) -> Callable[..., Any]:
        """Create shortcuts for registering functions in categories."""
        def create_shortcut(cat: str):
            def register_func(comment=None):
                return self.register_function(cat, comment)
            return register_func

        for category in categories:
            setattr(self, category, create_shortcut(category))

    def create_new_category(self, name: str) -> None:
        """Create a new category and its shortcut."""
        self.category_register.create_new_category(name)
        self._create_shortcuts_for_categories([name])

    def register_function(self, category: str, comment: Optional[str] = None) -> Callable[..., Any]:
        """Register a function in a specific category."""
        return self.category_register.register_function(category, comment)

    def is_valid_category(self, category_name: str) -> bool:
        """Check if the category name is valid."""
        return self.category_register.is_valid_category(category_name)

    def custom(self, category_name: str, comment: Optional[str] = None) -> Callable[..., Any]:
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
