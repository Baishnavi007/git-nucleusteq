"""
Question 7 - Parallel Execution

Convert a normal function
into parallel execution
using ThreadPoolExecutor.

ThreadPoolExecutor:
It creates and manages a pool
of worker threads to execute
tasks concurrently.
"""

from concurrent.futures import (
    ThreadPoolExecutor
)


def find_cube(value: int) -> int:
    """
    Return the cube
    of a value.
    """

    return value ** 3


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

        with ThreadPoolExecutor() as thread_pool:

            cube_results = thread_pool.map(
                find_cube,
                values
            )

        print("\nCubes:")

        for cube in cube_results:
            print(cube)