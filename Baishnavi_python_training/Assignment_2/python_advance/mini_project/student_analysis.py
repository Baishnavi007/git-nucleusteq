"""
Mini Project: Student Performance Analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_student_dataframe() -> pd.DataFrame:
    """
    Create and return student dataset.
    """

    student_data = {
        "Name": ["Rahul", "Priya", "Siri", "Anuj"],
        "Marks": [70, 80, 90, 60],
        "Hours Studied": [2, 3, 5, 1]
    }

    return pd.DataFrame(student_data)

def add_performance_column(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Add Pass/Fail column based on marks.
    """

    dataframe["Performance"] = dataframe["Marks"].apply(
        lambda marks: "Pass" if marks > 65 else "Fail"
    )

    return dataframe