"""
Assignment 6: Seaborn Visualizations

This module demonstrates:
1. Barplot
2. Boxplot
3. Heatmap
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def create_employee_dataframe() -> pd.DataFrame:
    """
    Create employee dataset.

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


def create_barplot(dataframe: pd.DataFrame) -> None:
    """
    Create barplot of department vs salary.
    """

    plt.figure(figsize=(6, 4))

    sns.barplot(
        data=dataframe,
        x="Department",
        y="Salary"
    )

    plt.title("Department vs Salary")
    plt.show()


def create_boxplot(dataframe: pd.DataFrame) -> None:
    """
    Create boxplot for salary distribution.
    """

    plt.figure(figsize=(6, 4))

    sns.boxplot(
        y=dataframe["Salary"]
    )

    plt.title("Salary Distribution")
    plt.show()


def create_heatmap(dataframe: pd.DataFrame) -> None:
    """
    Create heatmap using Age and Salary correlation.
    """

    correlation_matrix = dataframe[
        ["Age", "Salary"]
    ].corr()

    plt.figure(figsize=(5, 4))

    sns.heatmap(
        correlation_matrix,
        annot=True
    )

    plt.title("Age and Salary Correlation")
    plt.show()


def main() -> None:
    """
    Execute all seaborn visualizations.
    """

    employee_dataframe = create_employee_dataframe()

    create_barplot(employee_dataframe)

    create_boxplot(employee_dataframe)

    create_heatmap(employee_dataframe)


if __name__ == "__main__":
    main()