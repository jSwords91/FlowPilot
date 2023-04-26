# FlowPilot

FlowPilot is a package that helps Data Engineers and Data Scientists organize their code and effortlessly build pipelines. 

It encourages modular code, organizes projects effortlessly, and aids in production. With FlowPilot, you can tag your functions and automatically organize them into the appropriate directories. This makes it easy to manage your code and maintain your projects.

The tags we have built in currently are:
* data_reader
* data_writer
* data_transformer
* test
* custom

The key feature in FlowPilot is the tagging system:

```python 
@fp.data_reader(comment="Reads in a pandas dataframe")
def read(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)
```

Tag your functions and they become traceable, searchable, and reusable.

## Benefits of using FlowPilot

- **Modular code**: FlowPilot encourages you to write modular code. This makes it easier to test and maintain your code.

- **Easy organization**: FlowPilot automatically organizes your code into directories based on the tags you provide. This saves you time and effort and makes it easy to find what you need.

- **Reduced complexity**: FlowPilot's tagging & searching system simplifies the process of finding specific functions and understanding their purpose, making it easier to maintain and update a project over time.

- **Search & Discovery**: In large code based, it is difficult to find whether or not a function already exists for your needs. FLowPilot enables functions to be tagged and commented, and you can search for REGEX matches for either the name, comment, or function itself. If there's a match, FlowPilot tells you the function.

- **Pipelines**: Execute your code in the order it is intended.

- **Easy function registration**: FlowPilot provides a convenient way to register functions and associate them with a category and comment. This can help ensure that all functions are properly documented and categorized.

- **Script compilation**: FlowPilot can automatically generate Python scripts for each category based on the registered functions. This can save time and reduce errors when preparing scripts for deployment.

- **Custom categories**: FlowPilot allows for the creation of custom categories, so developers can easily extend the existing categories to suit their needs.

- **Project-level overview**: FlowPilot provides a way to display all registered functions in the project, along with their associated categories and comments. This can help developers get a high-level overview of the project and quickly identify any gaps in documentation or categories.


# Usage 

## Not yet ready for public use

To use FlowPilot, you need to import the package and create a FlowPilot object. Here's how you will soon be able to do it:

```python
from FlowPilot import *
```

## Tag your functions: Effortless Organisation & Pipeline Building

To tag your functions, you need to use the appropriate decorator provided by FlowPilot. 
The comment is mandatory to emphasise code readability for you and your colleagues.

Here's an example with some illustrative functions - note we've created a new category too which automatically creates a new directory.

We'll use the classic titanic dataset.


```python
import pandas as pd # for example only

fp = FlowPilot(project_name="TitanicProject")

@fp.data_reader(comment="Reads in a pandas dataframe")
def read(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)

@fp.data_transformer(comment="Filters dataset by gender")
def get_gender_only(df: pd.DataFrame, gender: str = "") -> pd.DataFrame:
    return df[df['Sex'] == gender]

@fp.data_transformer(comment="Calculates avg. age by survival")
def get_survivor_age(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(["Survived"])["Age"].mean()

@fp.data_transformer(comment="Calculates avg. fare by survival")
def get_survivor_fare(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(["Survived"])["Fare"].mean()

@fp.test(comment="Tests something...")
def test_read(df: pd.DataFrame) -> pd.DataFrame:
    """ Do some tests..."""
    return df

# For one off use, you can use the custom decorator
@fp.custom(category_name='data_evaluator', comment="Evaluates something...")
def evaluate(df: pd.DataFrame) -> pd.DataFrame:
    """Do some evaluation..."""
    return df

# If you are going to use a category repeatedly
fp.create_new_category(name="data_visualizer")

@fp.data_visualizer(comment="Visualize something...")
def plot_age_dist_by_pclass(df: pd.DataFrame) -> None:
    """Visualize something..."""
    
@fp.data_visualizer(comment="Visualize something else...")
def plot_survival(df: pd.DataFrame) -> None:
    """Visualize something esle..."""

```

Now we have tagged our functions in their categories.

## Display your registered functions
    
```python
fp.display_functions(category_name="data_transformer", include_function=False)
```

This will display all your functions registered in the data_transformer category along with their descriptions:

```python
{
    "functions": {
        "data_transformer": [
            {
                "name": "get_gender_only",
                "comment": "Filters dataset by gender",
                "function definition": "Not Displayed"
            },
            {
                "name": "get_survivor_age",
                "comment": "Calculates avg. age by survival",
                "function definition": "Not Displayed"
            },
            {
                "name": "get_survivor_fare",
                "comment": "Calculates avg. fare by survival",
                "function definition": "Not Displayed"
            }
        ]
    }
}

```

the default for fp.display_functions() is to display all registered functions.


It is also possible to search functions.

```python
fp.search_functions("calc*")
```

This would return 

```python
Search results:
Name: get_survivor_age, Category: data_transformer, Comment: Calculates avg. age by survival
Name: get_survivor_fare, Category: data_transformer, Comment: Calculates avg. fare by survival
```

In large code bases this is extremely useful. 

## Pipelines

Next, we can define a Pipeline. Notice how we can provide arguments for the functions too:

```python
pipeline = Pipeline(fp)
pipeline.add_step("data_reader", read, "./sample_data/titanic.csv")
pipeline.add_step("data_transformer", get_gender_only, "female")
pipeline.add_step("data_transformer", get_survivor_age)

# Now the pipeline executes in order
pipeline.execute()
```

And we can display the steps, too:

```python
pipeline.show_pipeline_steps()
```

Produces output:

```python
Pipeline steps:
1. [data_reader] read(./sample_data/titanic.csv)
2. [data_transformer] get_gender_only(female)
3. [data_transformer] get_survivor_age()
```

The UI/UX is still in development. 

Soon there will be DAG visialization and Pipeline validation build in to FlowPilot.

In addition, we will be building in parralel operation.

## Automatic Script Generation

Now you can compile these scripts in their respective folders:

```python
fp.write_category_to_file("all")

# We can also individual categories e.g. "data_reader"
```

This will create the following:

```
TitanicProject/
│
├── data_reader/
│   ├── data_reader.py
│
├── data_transformer/
│   ├── data_transformer.py
│
├── data_evaluator/
│   ├── data_evaluator.py
│
├── data_visualizer/
│   ├── data_visualizer.py
│
├── test/
│   ├── test.py

```


Each script file contains all imports defined in the project so each can be ran, regardless of links to other directories.

## Multiple Projects

It is also possible to create multiple project structures for further code segmentation:

```python
fpCRM = FlowPilot(project_name='new_CRM_project')

fpSales = FlowPilot(project_name='new_Sales_project')

@fpCRM.data_reader
def my_data_loader_for_crm():
    pass

@fpCRM.data_transformer
def my_preprocessor_for_crm():
    pass

@fpCRM.data_writer
def my_data_writer_for_crm():
    pass

@fpSales.data_reader
def my_data_loader_for_sales():
    pass


@fpSales.data_writer
def my_data_writer():
    pass

```
This will create the new structures.

# Features in Dev

- **Data quality constraints**: Add expectations to your pipelines

- **DAGs**: Visualize your pipeline

- **Call functions from FlowPilot**: E.g. fp.function_call(read, "input_arg") - allow the user to call functions they've discovered through the search system without having to import them manually.

## **Contributions welcome**
