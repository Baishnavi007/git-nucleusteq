"""
Question 8 - Parallel Execution

Convert a normal function
into parallel execution
using ProcessPoolExecutor.

ProcessPoolExecutor:
It creates and manages multiple
processes to execute CPU-intensive
tasks in parallel.
"""

from concurrent.futures import (
    ProcessPoolExecutor
)


def find_factorial(value: int) -> int:
    """
    Return the factorial
    of a value.
    """

    factorial = 1

    for number in range(
        1,
        value + 1
    ):
        factorial *= number

    return factorial


if __name__ == "__main__":

    entered_values = input(
        "Enter numbers separated by spaces: "
    )

    values = [
        int(item)
        for item in entered_values.split()
    ]

    if not values:
        print(
            "No values were provided."
        )

    else:

        with ProcessPoolExecutor() as process_pool:

            factorial_results = (
                process_pool.map(
                    find_factorial,
                    values
                )
            )

        print("\nFactorials:")

        for factorial in factorial_results:
            print(factorial)