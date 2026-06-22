"""
Question 7 - Regular Expressions

Write a pattern to check
if a string contains only
alphabets.
"""

import re


def is_alphabetic(word: str) -> bool:
    """
    Check whether the given
    string contains only letters.
    """

    # Match the entire string and allow
    # only uppercase or lowercase letters.
    alphabet_pattern = r"^[A-Za-z]+$"

    return bool(
        re.match(
            alphabet_pattern,
            word
        )
    )


if __name__ == "__main__":

    print(
        "\n--- Alphabet Checker ---"
    )

    user_input = input(
        "Enter a word: "
    )

    if is_alphabetic(user_input):
        print(
            "The input contains only letters."
        )
    else:
        print(
            "The input contains characters other than letters."
        )