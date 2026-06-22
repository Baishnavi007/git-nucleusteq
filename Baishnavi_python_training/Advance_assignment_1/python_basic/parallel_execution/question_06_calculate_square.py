"""
Question 6

Write a multiprocessing
program to calculate the
square of numbers using
the Process class.

Multiprocessing:
It enables multiple processes
to execute tasks independently.
"""

import multiprocessing


def display_square(value: int) -> None:
    """
    Compute and display
    the square of a value.
    """

    squared_value = value ** 2

    print(
        f"{value} squared is "
        f"{squared_value}"
    )


if __name__ == "__main__":

    user_values = input(
        "Enter numbers separated by spaces: "
    )

    values = [
        int(item)
        for item in user_values.split()
    ]

    if not values:
        print(
            "No input values provided."
        )

    else:

        active_processes = []

        for value in values:

            worker_process = (
                multiprocessing.Process(
                    target=display_square,
                    args=(value,)
                )
            )

            active_processes.append(
                worker_process
            )

            worker_process.start()

        for worker_process in active_processes:
            worker_process.join()