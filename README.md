# FlowPilot

FlowPilot is a package that helps Data Engineers and Data Scientists organize their code and effortlessly build pipelines. 

It encourages modular code, organizes projects effortlessly, and aids in production. With FlowPilot, you can tag your functions and automatically organize them into the appropriate directories. This makes it easy to manage your code and maintain your projects.

The newest addition to FlowPilot is Pipelines. This feature is shown below.

The tags we have currently are:
* data_reader
* data_writer
* data_transformer
* test
* custom

## **We are actively looking for contributions!**


## Benefits of using FlowPilot
**Modular code**: FlowPilot encourages you to write modular code by organizing your functions into separate files. This makes it easier to test and maintain your code.

**Easy organization**: FlowPilot automatically organizes your code into directories based on the tags you provide. This saves you time and effort and makes it easy to find what you need.

**Reduced complexity**: FlowPilot's tagging system simplifies the process of finding specific functions and understanding their purpose, making it easier to maintain and update a project over time.

**Pipelines**: Execute your code in the order it is intended.

**Production-ready code**: By using FlowPilot, you can ensure that your code is production-ready by organizing it in a way that is easy to manage and maintain.

**Easy function registration**: FlowPilot provides a convenient way to register functions and associate them with a category and comment. This can help ensure that all functions are properly documented and categorized.

**Script compilation**: FlowPilot can automatically generate Python scripts for each category based on the registered functions. This can save time and reduce errors when preparing scripts for deployment.

**Custom categories**: FlowPilot allows for the creation of custom categories, so developers can easily extend the existing categories to suit their needs.

**Project-level overview**: FlowPilot provides a way to display all registered functions in the project, along with their associated categories and comments. This can help developers get a high-level overview of the project and quickly identify any gaps in documentation or categories.


# Usage 

## Not yet ready for public use

To use FlowPilot, you need to import the package and create a FlowPilot object. Here's how you will soon be able to do it:

```python
import FlowPilot

```

## Tag your functions: Effortless Organisation & Pipeline Building

To tag your functions, you need to use the appropriate decorator provided by FlowPilot. 
The comment is mandatory to emphasise code readability for you and your colleagues.

Here's an example with some illustrative functions - note we've created a new category too.

We'll use titanic dataset.


```python
fp = FlowPilot(project_name="TitanicProject")


@fp.data_reader(comment="Reads in a pandas dataframe, defaults to titanic sample")
def read(filepath: str = "./sample_data/titanic.csv") -> pd.DataFrame:
    return pd.read_csv(filepath)

@fp.data_transformer(comment="Filters dataset to male only")
def get_males_only(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['Sex'] == "male"]

@fp.data_transformer(comment="Calculates avg. age by survival")
def get_survivor_age(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(["Survived"])["Age"].mean()

@fp.test(comment="Test reader")
def test_read(df: pd.DataFrame) -> pd.DataFrame:
    return df

# For one off use, you can use the custom decorator
@fp.custom(category_name='data_evaluator', comment="Evaluates models")
def evaluate(df: pd.DataFrame) -> pd.DataFrame:
    return df

# If you are going to use a category repeatedly
fp.create_new_category(name="data_visualize")

@fp.data_visualize(comment="Visualize dataset")
def visualize_df(df: pd.DataFrame) -> None:
    return None
```

Now we have tagged our functions to their categories.

## Display your registered functions
    
```python
fp.display_functions()
```

This will display all your functions registered in their categories along with their descriptions:

```python
{
    "functions": {
        "data_reader": [
            {
                "name": "read",
                "comment": "Reads in a pandas dataframe, defaults to titanic sample"
            }
        ],
        "data_transformer": [
            {
                "name": "get_males_only",
                "comment": "Filters dataset to male only"
            },
            {
                "name": "get_survivor_age",
                "comment": "Calculates avg. age by survival"
            }
        ],
        "test": [
            {
                "name": "test_read",
                "comment": "Test reader"
            }
        ],
        "data_evaluator": [
            {
                "name": "evaluate",
                "comment": "Evaluates models"
            }
        ],
        "data_visualize": [
            {
                "name": "visualize_df",
                "comment": "Visualize dataset"
            }
        ]
    }
}

```
## Pipelines

Next, we can define a Pipeline. 

```python
pipeline = Pipeline(fp)
pipeline.add_step("data_reader", "read")
pipeline.add_step("data_transformer", "get_males_only")
pipeline.add_step("data_transformer", "get_survivor_age")
pipeline.add_step("data_evaluator", "evaluate")

# Now the pipeline executes in order
pipeline.execute("./sample_data/titanic.csv")
```

The UI/UX is still in development. 

Soon there will be DAG visialization and Pipeline validation build in to FlowPilot.

In addition, we will be building in parralel operation.

## Automatic Script Generation

Now you can compile these scripts in their respective folders:

```python
fp.compile_scripts("all")

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
├── data_evaluator/
│   ├── data_evaluator.py
│
├── test/
│   ├── test.py

```

## Multiple Projects

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
This will create the new structures.


## We are actively looking for contributions!

