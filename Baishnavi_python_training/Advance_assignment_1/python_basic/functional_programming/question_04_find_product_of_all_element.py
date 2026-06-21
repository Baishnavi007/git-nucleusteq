"""
Question 4
Use reduce() to find the
product of all elements in a list.
"""

from functools import reduce

def find_product(numbers: list[int]) -> int:
    """
    Return the product of all
    elements using reduce().
    """

    
    if not numbers:
        raise ValueError(
            "The list cannot be empty."
        )

    # reduce() combines all values
    # into a single result.
    return reduce(
        lambda first, second: first * second,
        numbers
    )


if __name__ == "__main__":

    print("\n--- Find Product ---")

    numbers = [5, 2, 3, 4, 6]

    # Display the final product of all elements in a list.
    print(find_product(numbers))