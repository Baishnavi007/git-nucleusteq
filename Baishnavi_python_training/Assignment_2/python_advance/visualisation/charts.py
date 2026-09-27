"""
Assignment 5: Matplotlib Charts

This module demonstrates:
1. Bar Chart
2. Line Chart
3. Histogram
4. Scatter Plot
"""

import matplotlib.pyplot as plt


DEPARTMENTS = ["HR", "IT", "Finance"]
EMPLOYEE_COUNT = [5, 12, 7]

AGES = [25, 30, 28, 35]
SALARIES = [30000, 50000, 45000, 60000]


def create_bar_chart() -> None:
    """
    Create a bar chart showing employee count by department.
    """

    plt.figure(figsize=(6, 4))

    plt.bar(DEPARTMENTS, EMPLOYEE_COUNT)

    plt.title("Employees By Department")
    plt.xlabel("Department")
    plt.ylabel("Number Of Employees")

    plt.show()


def create_line_chart() -> None:
    """
    Create a line chart showing employee count trend.
    """

    plt.figure(figsize=(6, 4))

    plt.plot(DEPARTMENTS, EMPLOYEE_COUNT)

    plt.title("Department Employee Trend")
    plt.xlabel("Department")
    plt.ylabel("Number Of Employees")

    plt.show()


def create_histogram() -> None:
    """
    Create a histogram of salaries.
    """

    salary_data = [30000, 40000, 50000, 60000, 45000]

    plt.figure(figsize=(6, 4))

    plt.hist(salary_data)

    plt.title("Salary Distribution")
    plt.xlabel("Salary")
    plt.ylabel("Frequency")

    plt.show()


def create_scatter_plot() -> None:
    """
    Create scatter plot of age vs salary.
    """

    plt.figure(figsize=(6, 4))

    plt.scatter(AGES, SALARIES)

    plt.title("Age Vs Salary")
    plt.xlabel("Age")
    plt.ylabel("Salary")

    plt.show()


def main() -> None:
    """
    Execute all chart creation tasks.
    """

    create_bar_chart()

    create_line_chart()

    create_histogram()

    create_scatter_plot()


if __name__ == "__main__":
    main()