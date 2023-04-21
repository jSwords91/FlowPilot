# FlowPilot
A package to help Data Engineers and Data Scientists organise their code

# Organise your code automatically


## Import

`!pip install flow-pilot`

`import FlowPilot`

## Initiate `FlowPilot` Object

`fp = FlowPilot()`

## Tag your functions

`@fp.data_loader
def my_data_loader():
    pass`
    
`@fp.test
def test_function_x():
pass`
    
    
This will write your functions in to the appropriate folders.

# To Do:

* Testing
* Add user defined function path rather then only default current directory