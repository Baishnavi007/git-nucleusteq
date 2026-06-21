"""
Question 7 - Functional Programming

Convert a simple loop-based program
into a functional style using filter().
"""


def get_even_numbers(numbers: list[int]) -> list[int]:
    """
    Return only even numbers
    from the given list.
    """

    # Traditional loop approach:
    # even_numbers = []
    # for number in numbers:
    #     if number % 2 == 0:
    #         even_numbers.append(number)

    # filter() keeps only values
    # that satisfy the condition.
    return list(
        filter(
            lambda number: number % 2 == 0,
            numbers
        )
    )


if __name__ == "__main__":

    print(
        "\n--- Functional Style Example ---"
    )

    values = [11, 20, 35, 42, 57, 68]

    print(
        get_even_numbers(values)
    )