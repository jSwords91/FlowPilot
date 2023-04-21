import os
import shutil
from typing import Callable
import sys

# Add the FlowPilot folder to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "FlowPilot")))

# Import the module
from flow_pilot import FlowPilot


def test_data_loader():
    # Create a FlowPilot instance and define a test data loader function
    fp = FlowPilot(project_name="my_project")
    @fp.data_loader
    def load_data():
        pass
    
    # Check that the function was saved to the correct directory
    file_path = os.path.join("my_project", "data_loader", "load_data.py")
    assert os.path.exists(file_path)
    
    # Clean up the directory
    shutil.rmtree("my_project")
    
def test_data_writer():
    # Create a FlowPilot instance and define a test data loader function
    fp = FlowPilot(project_name="my_project")
    @fp.data_writer
    def write_data():
        pass
    
    # Check that the function was saved to the correct directory
    file_path = os.path.join("my_project", "data_writer", "write_data.py")
    assert os.path.exists(file_path)
    
    # Clean up the directory
    shutil.rmtree("my_project")
    

def test_preprocessor():
    # Create a FlowPilot instance and define a test preprocessor function
    fp = FlowPilot(project_name="my_project")
    @fp.preprocessor
    def preprocess_data():
        pass
    
    # Check that the function was saved to the correct directory
    file_path = os.path.join("my_project", "preprocessor", "preprocess_data.py")
    assert os.path.exists(file_path)
    
    # Clean up the directory
    shutil.rmtree("my_project")
    

def test_model_training():
    # Create a FlowPilot instance and define a test model training function
    fp = FlowPilot(project_name="my_project")
    @fp.model_training
    def train_model():
        pass
    
    # Check that the function was saved to the correct directory
    file_path = os.path.join("my_project", "model_training", "train_model.py")
    assert os.path.exists(file_path)
    
    # Clean up the directory
    shutil.rmtree("my_project")
    

def test_data_viz():
    # Create a FlowPilot instance and define a test data visualization function
    fp = FlowPilot(project_name="my_project")
    @fp.data_viz
    def visualize_data():
        pass
    
    # Check that the function was saved to the correct directory
    file_path = os.path.join("my_project", "data_viz", "visualize_data.py")
    assert os.path.exists(file_path)
    
    # Clean up the directory
    shutil.rmtree("my_project")
    

def test_test():
    # Create a FlowPilot instance and define a test function
    fp = FlowPilot(project_name="my_project")
    @fp.test
    def test_multiply_by_two():
        assert multiply_by_two(4) == 8
    
    # Check that the function was saved to the correct directory
    file_path = os.path.join("my_project", "tests", "test_multiply_by_two.py")
    assert os.path.exists(file_path)
    
    # Clean up the directory
    shutil.rmtree("my_project")
