# FlowPilot
A package to help Data Engineers and Data Scientists organise their code.

This encourages modular code, organises projects effortlessly, and aids in production.

# Organise your code automatically

## Import

`!pip install flow-pilot`

`import FlowPilot`

## Initiate `FlowPilot` Object

`fp = FlowPilot()`

## Tag your functions


```python
@fp.data_loader
def my_data_loader():
    pass

@fp.test
def test_function_x():
    pass
```
    
This will write your functions in to the appropriate folders.

The tags we have currently are:
* data_loader
* preprocessor
* test
* model_training
* data_viz


# To Do:

* Testing
* Add user defined function path rather then only default current directory