"""
Question 6:

Replace multiple spaces in a
string with a single space
using re.sub().
"""

import re


def normalize_spacing(sentence: str) -> str:
    """
    Replace extra spaces in a
    string with a single space.
    """

    # Replace consecutive whitespace
    # characters with a single space.

    # \s+ matches one or more whitespace characters.
    # re.sub() replaces each matching sequence with one space.
    return re.sub(r"\s+", " ", sentence)


if __name__ == "__main__":

    print("\n--- Space Normalization Example ---")

    user_text = input(
        "Enter a sentence: "
    )

    formatted_text = normalize_spacing(
        user_text
    )

    print(
        f"Formatted Text: "
        f"{formatted_text}"
    )