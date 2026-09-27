"""
Question 1

Write a program to extract all numbers
from a given string using regular expressions.
"""

import re


def extract_numbers(text: str) -> list[str]:
    """
    Return all numbers found in a string.
    """

    # findall() it  returns all values
    # \d+  it matches one or more digits.
    return re.findall(r"\d+", text)


if __name__ == "__main__":

    print("\n--- Numbers Extracted ---")

    text = "My age is 22 , and i was born in 2003, and my brother is 28 years old."

    # Print all numbers found in the givenstring.
    print(extract_numbers(text))