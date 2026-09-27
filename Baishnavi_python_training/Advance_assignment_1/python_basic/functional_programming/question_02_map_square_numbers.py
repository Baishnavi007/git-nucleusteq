"""
Question 2 - Functional Programming

Use map() to convert a list
of numbers into their squares.
"""


def get_squared_numbers(numbers: list[int]) -> list[int]:
    """
    Return square values of the given list of numbers
    using map().
    """

    # map() applies the square operation to each and every element of the list
    return list(map(lambda number: number ** 2, numbers))


if __name__ == "__main__":

    print("\n--- Sample Map Example ---")

    numbers = [5, 6, 7, 8, 9]

    # Display squared values that gets generated using map().
    print(get_squared_numbers(numbers))