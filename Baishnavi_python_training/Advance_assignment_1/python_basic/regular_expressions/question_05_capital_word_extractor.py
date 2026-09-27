"""
Question 5: 
Program to extract all words
starting with a capital letter.
"""

import re


CAPITAL_WORD_PATTERN: str = r"\b[A-Z][a-zA-Z]*\b"


def extract_capital_words(
        text: str
) -> list[str]:
    """
    Extract words that start
    with a capital letter.
    """

    return re.findall(
        CAPITAL_WORD_PATTERN,
        text
    )


def main() -> None:
    """
    Execute the program.
    """

    text = input(
        "Enter a sentence: "
    )

    capital_words = (
        extract_capital_words(
            text
        )
    )

    print(
        f"Capital Words: {capital_words}"
    )


if __name__ == "__main__":
    main()