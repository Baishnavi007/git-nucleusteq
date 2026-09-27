"""
Question 8 - Regular Expressions

Create a password validation
program using regex.
"""

import re


def validate_password(user_password: str) -> bool:
    """
    Validate whether the password
    satisfies the required rules.
    """

    # Ensure the password contains:
    # - at least one uppercase letter
    # - at least one digit
    # - at least one special character
    # - minimum length of 8 characters
    password_pattern = (
        r"^(?=.*[A-Z])"
        r"(?=.*\d)"
        r"(?=.*[@#$%&!])"
        r".{8,}$"
    )

    return bool(
        re.match(
            password_pattern,
            user_password
        )
    )


if __name__ == "__main__":

    print(
        "\n--- Password Strength Checker ---"
    )

    entered_password = input(
        "Enter a password: "
    )

    if validate_password(
        entered_password
    ):
        print(
            "Password is valid."
        )
    else:
        print(
            "Invalid password. "
            "It must contain at least "
            "8 characters, one uppercase letter, "
            "one digit, and one special character."
        )