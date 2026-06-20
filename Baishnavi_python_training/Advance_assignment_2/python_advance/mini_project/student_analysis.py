"""
Assignment 7: Student Performance Analysis

This mini project demonstrates:
1. Creating a Pandas DataFrame
2. Adding a new column using conditional logic
3. Creating Matplotlib visualizations
4. Creating Seaborn visualizations
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def create_student_dataframe() -> pd.DataFrame:
    """
    Create and return a student dataset.

    Returns:
        pd.DataFrame: Student information.
    """

    student_data = {
        "Name": ["Rahul", "Priya", "Siri", "Anuj"],
        "Marks": [70, 80, 90, 60],
        "Hours Studied": [2, 3, 5, 1]
    }

    return pd.DataFrame(student_data)


def add_performance_column(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Add a Performance column based on student marks.

    Pass -> Marks > 65
    Fail -> Marks <= 65

    Args:
        dataframe (pd.DataFrame): Student DataFrame.

    Returns:
        pd.DataFrame: Updated DataFrame.
    """

    dataframe["Performance"] = dataframe["Marks"].apply(
        lambda marks: "Pass" if marks > 65 else "Fail"
    )

    return dataframe


def display_basic_statistics(dataframe: pd.DataFrame) -> None:
    """
    Display basic statistics about student marks.

    Args:
        dataframe (pd.DataFrame): Student DataFrame.
    """

    print("\nAverage Marks:")
    print(dataframe["Marks"].mean())

    print("\nHighest Marks:")
    print(dataframe["Marks"].max())

    print("\nLowest Marks:")
    print(dataframe["Marks"].min())


def create_line_chart(dataframe: pd.DataFrame) -> None:
    """
    Create a line chart showing Hours Studied vs Marks.

    Args:
        dataframe (pd.DataFrame): Student DataFrame.
    """

    plt.figure(figsize=(6, 4))

    plt.plot(
        dataframe["Hours Studied"],
        dataframe["Marks"],
        marker="o"
    )

    plt.title("Hours Studied vs Marks")
    plt.xlabel("Hours Studied")
    plt.ylabel("Marks")

    plt.show()


def create_scatter_plot(dataframe: pd.DataFrame) -> None:
    """
    Create a scatter plot showing Hours Studied vs Marks.

    Args:
        dataframe (pd.DataFrame): Student DataFrame.
    """

    plt.figure(figsize=(6, 4))

    plt.scatter(
        dataframe["Hours Studied"],
        dataframe["Marks"]
    )

    plt.title("Study Hours vs Marks")
    plt.xlabel("Hours Studied")
    plt.ylabel("Marks")

    plt.show()


def create_performance_barplot(dataframe: pd.DataFrame) -> None:
    """
    Create a Seaborn barplot showing Performance vs Marks.

    Args:
        dataframe (pd.DataFrame): Student DataFrame.
    """

    plt.figure(figsize=(6, 4))

    sns.barplot(
        data=dataframe,
        x="Performance",
        y="Marks"
    )

    plt.title("Performance vs Marks")

    plt.show()


def main() -> None:
    """
    Execute all mini project tasks.
    """

    # Create dataset
    student_dataframe = create_student_dataframe()

    print("Original Dataset:")
    print(student_dataframe)

    # Add performance column
    student_dataframe = add_performance_column(
        student_dataframe
    )

    print("\nUpdated Dataset:")
    print(student_dataframe)

    # Display statistics
    display_basic_statistics(student_dataframe)

    # Create visualizations
    create_line_chart(student_dataframe)

    create_scatter_plot(student_dataframe)

    create_performance_barplot(student_dataframe)


if __name__ == "__main__":
    main()