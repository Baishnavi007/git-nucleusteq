"""
Question 4

Use pdb breakpoints inside
a loop and inspect
variable values.
"""

import pdb


def display_countdown() -> None:
    """
    Display numbers from
    1 to 5.
    """

    for current_number in range(
        1,
        6
    ):
        pdb.set_trace()

        print(
            f"Current Number: "
            f"{current_number}"
        )


if __name__ == "__main__":

    display_countdown()