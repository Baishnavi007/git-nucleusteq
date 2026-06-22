"""
Question 4 

Use re.search() to check whether a word exists in a sentence.
"""

import re


def word_present(sentence: str, word: str) -> bool:
    """
    Return True if the word exists.
    else false
    """
    
    # re.escape() treats special regex characters as normal text.
    # re.search() checks whether the word is present.
    # re.IGNORECASE makes the search case-insensitive.
    return bool(re.search(re.escape(word), sentence, re.IGNORECASE))


if __name__ == "__main__":

    print("\n--- Word Find ---")

    sentence = "Machine learning is a subset of artificial intelligence."
    word = input("Enter the word to search: ")

    # Display search result.
    if word_present(sentence, word):
        print("Word found in the sentence.")
    else:
        print("Word not found.")