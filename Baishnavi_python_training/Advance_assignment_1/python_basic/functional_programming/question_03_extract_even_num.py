"""
Question 3 - Functional Programming

Use filter() to extract
even numbers from a list.
"""


def get_even_numbers(numbers: list[int]) -> list[int]:
    """
    Return even numbers
    using filter().
    """

    # filter() keeps only values that satisfy the specific condition.
    return list(filter(lambda number: number % 2 == 0, numbers))


if __name__ == "__main__":

    print("\n--- Extract Even Numbers ---")

    numbers = [11, 22, 43, 44, 55, 66, 47, 90, 8]

    # Display only the even numbers from the list.
    print(get_even_numbers(numbers))