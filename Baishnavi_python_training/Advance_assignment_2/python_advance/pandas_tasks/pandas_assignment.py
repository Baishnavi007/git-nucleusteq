"""
Assignment 2: Pandas DataFrame Operations

This module demonstrates:
1. DataFrame creation
2. Viewing records
3. Summary statistics
4. Filtering data
5. Creating new columns
"""

import pandas as pd


def create_employee_dataframe() -> pd.DataFrame:
    """
    Create and return employee DataFrame.

    Returns:
        pd.DataFrame: Employee information
    """

    employee_data = {
        "Name": ["Rahul", "Priya", "Amit", "Anuj"],
        "Age": [25, 30, 28, 35],
        "Department": ["HR", "IT", "Finance", "IT"],
        "Salary": [30000, 50000, 45000, 60000]
    }

    return pd.DataFrame(employee_data)


def display_first_two_rows(dataframe: pd.DataFrame) -> None:
    """
    Display first two rows of DataFrame.
    """

    print("\nFirst Two Rows:")
    print(dataframe.head(2))


def display_summary_statistics(dataframe: pd.DataFrame) -> None:
    """
    Display summary statistics.
    """

    print("\nSummary Statistics:")
    print(dataframe.describe())


def display_it_employees(dataframe: pd.DataFrame) -> None:
    """
    Display only employees from IT department.
    """

    it_employees = dataframe[dataframe["Department"] == "IT"]

    print("\nIT Employees:")
    print(it_employees)


def add_bonus_column(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Add bonus column based on salary.

    Returns:
        pd.DataFrame: Updated DataFrame
    """

    # Bonus is 10 percent of salary
    dataframe["Bonus"] = dataframe["Salary"] * 0.10

    return dataframe


def main() -> None:
    """
    Execute all Assignment 2 tasks.
    """

    employee_dataframe = create_employee_dataframe()

    print("Employee Data:")
    print(employee_dataframe)

    display_first_two_rows(employee_dataframe)

    display_summary_statistics(employee_dataframe)

    display_it_employees(employee_dataframe)

    employee_dataframe = add_bonus_column(employee_dataframe)

    print("\nDataFrame With Bonus:")
    print(employee_dataframe)


if __name__ == "__main__":
    main()