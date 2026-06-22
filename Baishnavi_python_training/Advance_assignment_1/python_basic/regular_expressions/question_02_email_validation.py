"""
Question 2 - Regular Expressions

Write a regex pattern to
validate an email address.
"""

import re


def is_valid_email(email: str) -> bool:
    """
    Return True if the email format is valid otherwise false.
    """

    # ^           -> Starting of string
    # [\w.-]+     -> Username 
    # @           ->  @ symbol is mandatory
    # [\w.-]+     -> Domain name
    # \.          -> Dot before extension
    # \w+         -> Domain extension
    # $           -> End of string
    model = r"^[\w.-]+@[\w.-]+\.\w+$"

    return bool(re.match(model, email))


if __name__ == "__main__":

    print("\n--- Email Validation ---")

    email = input("Enter your email: ")

    if is_valid_email(email):
        print("This is a valid email address.")
    else:
        print("This is an invalid email address.")