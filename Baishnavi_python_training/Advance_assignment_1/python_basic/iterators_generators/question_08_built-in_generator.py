"""
Question 8

Show an example of a built-in generator
and iterate over it.
"""


if __name__ == "__main__":

    print(
        "\n--- Example of built-in generator ---"
    )

    # Create a range object.from 1 to n-1 i.e.9
    numbers = range(1, 10)

    # Print each value from the given range.
    for number in numbers:
        print(number)
