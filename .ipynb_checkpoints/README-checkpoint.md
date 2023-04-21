# FlowPilot

FlowPilot is a package that helps Data Engineers and Data Scientists organize their code. It encourages modular code, organizes projects effortlessly, and aids in production. With FlowPilot, you can tag your functions and automatically organize them into the appropriate directories. This makes it easy to manage your code and maintain your projects.

## Benefits of using FlowPilot
**Modular code**: FlowPilot encourages you to write modular code by organizing your functions into separate files. This makes it easier to test and maintain your code.

**Easy organization**: FlowPilot automatically organizes your code into directories based on the tags you provide. This saves you time and effort and makes it easy to find what you need.

**Reduced complexity**: FlowPilot's tagging system simplifies the process of finding specific functions and understanding their purpose, making it easier to maintain and update a project over time.

**Production-ready code**: By using FlowPilot, you can ensure that your code is production-ready by organizing it in a way that is easy to manage and maintain.

## *Organise your code automatically*

# Usage

## Install

`!pip install flow-pilot`

## Import & Initiate `FlowPilot` Object

To use FlowPilot, you need to import the package and create a FlowPilot object. Here's how you can do it:

```python
import FlowPilot

fp = FlowPilot()`

```

## Tag your functions

To tag your functions, you need to use the appropriate decorator provided by FlowPilot. Here's an example:


```python
@fp.data_loader
def my_data_loader():
    pass

@fp.test
def test_function_x():
    pass
```
    
This will write your functions in to the appropriate folders. For example:

```
Project/
│
├── data_loader/
│   ├── my_data_loader.py
|
├── tests/
│   ├── test_function_x.py
│
```


It is also possible to create a new project structure:

```python
fp = FlowPilot(project_name='new_project')

@fp.data_loader
def my_data_loader():
    pass

@fp.test
def test_function_x():
    pass


```
This will create a new structure

```
new_project/
│
├── data_loader/
│   ├── my_data_loader.py
|
├── tests/
│   ├── test_function_x.py
│
```


Alternatively, after the pip install:

```python
from FlowPilot import *


@data_loader
def my_data_loader():
    pass

@test
def test_function_x():
    pass
```

This will again use the standard functionality and write to the current directory.

The tags we have currently are:
* data_loader
* preprocessor
* test
* model_training
* data_viz


# To Do:

* Testing
* Add user defined function path rather then only default current directory