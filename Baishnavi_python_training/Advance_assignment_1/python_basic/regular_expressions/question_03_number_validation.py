"""
Question 3

Write a regular expression to
validate a 10-digit mobile number.
"""

import re


def is_valid_mobile_number(mobile_number: str) -> bool:
    """
    Return True if the mobile number is valid.
    """

    # ^      -> Starting of string
    # \d{10} -> Number of digits should be exactly 10
    # $      -> End of string
    pattern = r"^\d{10}$"

    return bool(re.match(pattern, mobile_number))


if __name__ == "__main__":

    print("\n--- Mobile Number Validation ---")

    mobile_number = input(
        "Enter mobile number: "
    )

    if is_valid_mobile_number(mobile_number):
        print("This is a valid mobile number.")
    else:
        print("This is an invalid mobile number.")