# FlowPilot

FlowPilot is a package that helps Data Engineers and Data Scientists organize their code. It encourages modular code, organizes projects effortlessly, and aids in production. With FlowPilot, you can tag your functions and automatically organize them into the appropriate directories. This makes it easy to manage your code and maintain your projects.

## Benefits of using FlowPilot
**Modular code**: FlowPilot encourages you to write modular code by organizing your functions into separate files. This makes it easier to test and maintain your code.

**Easy organization**: FlowPilot automatically organizes your code into directories based on the tags you provide. This saves you time and effort and makes it easy to find what you need.

**Reduced complexity**: FlowPilot's tagging system simplifies the process of finding specific functions and understanding their purpose, making it easier to maintain and update a project over time.

**Production-ready code**: By using FlowPilot, you can ensure that your code is production-ready by organizing it in a way that is easy to manage and maintain.

**Easy function registration**: FlowPilot provides a convenient way to register functions and associate them with a category and comment. This can help ensure that all functions are properly documented and categorized.

**Script compilation**: FlowPilot can automatically generate Python scripts for each category based on the registered functions. This can save time and reduce errors when preparing scripts for deployment.

**Custom categories**: FlowPilot allows for the creation of custom categories, so developers can easily extend the existing categories to suit their needs.

**Project-level overview**: FlowPilot provides a way to display all registered functions in the project, along with their associated categories and comments. This can help developers get a high-level overview of the project and quickly identify any gaps in documentation or categories.

## *Organise your code automatically*

# Usage 

## Not yet ready for public use

To use FlowPilot, you need to import the package and create a FlowPilot object. Here's how you can do it:

```python
import FlowPilot

fp = FlowPilot(project_name='Sales')

```

## Tag your functions

To tag your functions, you need to use the appropriate decorator provided by FlowPilot. 
The comment is mandatory to emphasise code readability for you and your colleagues.

Here's an example with some illustrative functions - note we've created a new category too:


```python
@fp.data_reader(comment='pulls data from abc.com api')
def read_api():
    return "API_READ"

@fp.data_reader(comment='Load all from source X')
def read(file_path):
    return "Success"

@fp.data_cleaner(comment='Removes null values')
def remove_null():
    return "Nulls Removed"

@fp.data_cleaner(comment='Removes blank values')
def remove_blank():
    return "Blanks Removed"

@fp.custom(category_name='modelling', comment='Tests loader function')
def test_func():
    return "Tests performed"

fp.display_functions()
```
    
This will display all your functions registered in their categories:

```python
{
    "project_name": "Sales",
    "functions": {
        "data_reader": [
            {
                "name": "read_api",
                "comment": "pulls data from abc.com api"
            },
            {
                "name": "read",
                "comment": "Load all from source X"
            }
        ],
        "data_cleaner": [
            {
                "name": "remove_null",
                "comment": "Removes null values"
            },
            {
                "name": "remove_blank",
                "comment": "Removes blank values"
            }
        ],
        "modelling": [
            {
                "name": "test_func",
                "comment": "Tests loader function"
            }
        ]
    }
}
```

Now you can compile these scripts in their respective folders:

```python
fp.compile_scripts("all")
```

This will create the following:

```
Sales/
│
├── data_reader/
│   ├── data_reader.py
│
├── data_cleaner/
│   ├── data_cleaner.py
│
├── modelling/
│   ├── modelling.py

```

It is also possible to create multiple project structures for further code segmentation:

```python
fpCRM = FlowPilot(project_name='new_CRM_project')

fpSales = FlowPilot(project_name='new_Sales_project')

@fpCRM.data_loader
def my_data_loader_for_crm():
    pass

@fpCRM.preprocessor
def my_preprocessor_for_crm():
    pass

@fpCRM.data_writer
def my_data_writer_for_crm():
    pass

@fpSales.data_loader
def my_data_loader_for_sales():
    pass


@fpSales.data_writer
def my_data_writer():
    pass

```
This will create the new structures



The tags we have currently are:
* data_reader
* data_writer
* data_cleaner
* custom

