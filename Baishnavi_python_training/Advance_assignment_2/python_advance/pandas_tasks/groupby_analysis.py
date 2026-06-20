"""
Assignment 4: GroupBy Analysis

This module demonstrates:
1. Average salary by department
2. Maximum salary by department
3. Employee count by department
"""

import pandas as pd


def create_employee_dataframe() -> pd.DataFrame:
    """
    Create employee DataFrame.

    Returns:
        pd.DataFrame: Employee information
    """

    employee_data = {
        "Name": ["Rahul", "Priya", "Amit", "Anuj"],
        "Department": ["HR", "IT", "Finance", "IT"],
        "Salary": [30000, 50000, 45000, 60000]
    }

    return pd.DataFrame(employee_data)


def calculate_average_salary(dataframe: pd.DataFrame) -> None:
    """
    Display average salary by department.
    """

    average_salary = dataframe.groupby("Department")["Salary"].mean()

    print("\nAverage Salary By Department:")
    print(average_salary)


def calculate_max_salary(dataframe: pd.DataFrame) -> None:
    """
    Display maximum salary by department.
    """

    maximum_salary = dataframe.groupby("Department")["Salary"].max()

    print("\nMaximum Salary By Department:")
    print(maximum_salary)


def count_employees(dataframe: pd.DataFrame) -> None:
    """
    Display employee count by department.
    """

    employee_count = dataframe.groupby("Department")["Name"].count()

    print("\nEmployee Count By Department:")
    print(employee_count)


def main() -> None:
    """
    Execute GroupBy analysis tasks.
    """

    employee_dataframe = create_employee_dataframe()

    print("Employee Data:")
    print(employee_dataframe)

    calculate_average_salary(employee_dataframe)

    calculate_max_salary(employee_dataframe)

    count_employees(employee_dataframe)


if __name__ == "__main__":
    main()