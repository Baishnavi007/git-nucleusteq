"""
Assignment 3: Data Cleaning

This module demonstrates:
1. Detecting missing values
2. Replacing missing age with mean age
3. Replacing missing salary with 0
"""

import pandas as pd
import numpy as np


def create_dataframe() -> pd.DataFrame:
    """
    Create DataFrame containing missing values.

    Returns:
        pd.DataFrame: Sample employee data
    """

    employee_data = {
        "Name": ["Rahul", "Priya", "Anuj"],
        "Age": [25, np.nan, 29],
        "Salary": [30000, 40000, np.nan]
    }

    return pd.DataFrame(employee_data)


def detect_missing_values(dataframe: pd.DataFrame) -> None:
    """
    Display missing values in DataFrame.
    """

    print("\nMissing Values:")
    print(dataframe.isnull())


def replace_missing_age(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Replace missing age with average age.

    Args:
        dataframe (pd.DataFrame): Input DataFrame

    Returns:
        pd.DataFrame: Updated DataFrame
    """

    mean_age = dataframe["Age"].mean()

    dataframe["Age"] = dataframe["Age"].fillna(mean_age)

    return dataframe


def replace_missing_salary(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Replace missing salary with 0.

    Args:
        dataframe (pd.DataFrame): Input DataFrame

    Returns:
        pd.DataFrame: Updated DataFrame
    """

    dataframe["Salary"] = dataframe["Salary"].fillna(0)

    return dataframe


def main() -> None:
    """
    Execute data cleaning operations.
    """

    employee_dataframe = create_dataframe()

    print("Original DataFrame:")
    print(employee_dataframe)

    detect_missing_values(employee_dataframe)

    employee_dataframe = replace_missing_age(employee_dataframe)

    employee_dataframe = replace_missing_salary(employee_dataframe)

    print("\nCleaned DataFrame:")
    print(employee_dataframe)


if __name__ == "__main__":
    main()