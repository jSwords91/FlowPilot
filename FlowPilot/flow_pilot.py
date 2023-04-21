import os
from typing import Callable, Any

import os
from typing import Callable, Any, Optional

class FlowPilot:
    def __init__(self, project_name: Optional[str] = None):
        self.project_name = project_name

    def _get_file_name(self, func: Callable) -> str:
        """Get the name of the file to save the function."""
        return f"{func.__name__}.py"

    def _make_file_path(self, dir_path: str, file_name: str) -> str:
        """Create the full file path for the function."""
        return os.path.join(dir_path, file_name)

    def _file_writer(self, func: Callable, dir_path: str) -> Callable[..., Any]:
        """Write the function to a file in the specified directory."""
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        # Create the directory if it doesn't exist
        if self.project_name:
            dir_path = os.path.join(self.project_name, dir_path)

        try:
            os.makedirs(dir_path, exist_ok=True)
        except OSError:
            raise OSError(f"Could not create directory {dir_path}")

        # Define the name of the file where the function will be stored
        file_name: str = self._get_file_name(func)

        # Define the full file path where the function will be stored
        file_path: str = self._make_file_path(dir_path, file_name)

        # Write the function to the file path
        try:
            with open(file_path, 'w') as f:
                f.write(f'def {func.__name__}({", ".join(func.__code__.co_varnames)}):\n')
                f.write(f'    pass')
        except IOError as e:
            print(f"An error occurred while writing to the file: {e}")

        return wrapper

    def data_loader(self, func: Callable) -> Callable[..., Any]:
        """Tag a function as a data loader and save it in the 'data_loader' directory."""
        dir_path: str = 'data_loader'
        return self._file_writer(func, dir_path)

    def preprocessor(self, func: Callable) -> Callable[..., Any]:
        """Tag a function as a preprocessor and save it in the 'preprocessor' directory."""
        dir_path: str = 'preprocessor'
        return self._file_writer(func, dir_path)

    def model_training(self, func: Callable) -> Callable[..., Any]:
        """Tag a function as a model trainer and save it in the 'model_training' directory."""
        dir_path: str = 'model_training'
        return self._file_writer(func, dir_path)

    def data_viz(self, func: Callable) -> Callable[..., Any]:
        """Tag a function as a data visualizer and save it in the 'data_viz' directory."""
        dir_path: str = 'data_viz'
        return self._file_writer(func, dir_path)

    def test(self, func: Callable) -> Callable[..., Any]:
        """Tag a function as a test function and save it in the 'tests' directory."""
        dir_path: str = 'tests'
        return self._file_writer(func, dir_path)


    
##### Individual functions ####
def _get_file_name(func: Callable) -> str:
    """Get the name of the file to save the function."""
    return f"{func.__name__}.py"

def _make_file_path(dir_path: str, file_name: str) -> str:
    """Create the full file path for the function."""
    return os.path.join(dir_path, file_name)

def file_writer(func: Callable, dir_path: str) -> Callable[..., Any]:
    """Write the function to a file in the specified directory."""
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)
    
    # Create the directory if it doesn't exist
    try:
        os.makedirs(dir_path, exist_ok=True)
    except OSError:
        raise OSError(f"Could not create directory {dir_path}")
    
    # Define the name of the file where the function will be stored
    file_name: str = _get_file_name(func)
    
    # Define the full file path where the function will be stored
    file_path: str = _make_file_path(dir_path, file_name)
    
    # Write the function to the file path
    try:
        with open(file_path, 'w') as f:
            f.write(f'def {func.__name__}({", ".join(func.__code__.co_varnames)}):\n')
            f.write(f'    pass')
    except IOError as e:
            print(f"An error occurred while writing to the file: {e}")

    return wrapper


def data_loader(func: Callable) -> Callable[..., Any]:
    """Tag a function as a data loader and save it in the 'data_loader' directory."""
    dir_path: str = './data_loader'
    return file_writer(func, dir_path)

def preprocessor(func: Callable) -> Callable[..., Any]:
    """Tag a function as a preprocessor and save it in the 'preprocessor' directory."""
    dir_path: str = './preprocessor'
    return file_writer(func, dir_path)

def model_training(func: Callable) -> Callable[..., Any]:
    """Tag a function as a model trainer and save it in the 'model_training' directory."""
    dir_path: str = './model_training'
    return file_writer(func, dir_path)

def data_viz(func: Callable) -> Callable[..., Any]:
    """Tag a function as a data visualizer and save it in the 'data_viz' directory."""
    dir_path: str = './data_viz'
    return file_writer(func, dir_path)


def test(func: Callable) -> Callable[..., Any]:
    """Tag a function as a test function and save it in the 'tests' directory."""
    dir_path: str = './tests'
    return file_writer(func, dir_path)
