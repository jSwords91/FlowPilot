# FlowPilot
A package to help Data Engineers and Data Scientists organise their code.

This encourages modular code, organises projects effortlessly, and aids in production.

## *Organise your code automatically*

# Usage

## Install

`!pip install flow-pilot`

## Import & Initiate `FlowPilot` Object

```python
import FlowPilot

fp = FlowPilot()`

```

In future you will be able to define a custom directory here rather than defaulting to `./`

## Tag your functions


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

The tags we have currently are:
* data_loader
* preprocessor
* test
* model_training
* data_viz


# To Do:

* Testing
* Add user defined function path rather then only default current directory