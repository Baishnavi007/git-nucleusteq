"""
Question 2 

Create a thread that
calculates the sum of
numbers from 1 to 100.
"""

import threading

LOWER_LIMIT = 1
UPPER_LIMIT = 100


def compute_total() -> None:
    """
    Calculate and display
    the total of the given range.
    """

    # Validate the range before processing.
    if LOWER_LIMIT > UPPER_LIMIT:
        print("Range is not valid.")
        return

    range_sum = sum(
        range(
            LOWER_LIMIT,
            UPPER_LIMIT + 1
        )
    )

    print(
        f"Total Sum: {range_sum}"
    )


if __name__ == "__main__":

    # Create a separate thread
    # for the calculation task.
    worker_thread = threading.Thread(
        target=compute_total
    )

    worker_thread.start()

    # Wait until the calculation
    # finishes before exiting.
    worker_thread.join()