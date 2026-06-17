"""
Programs demonstrating Python modules.
"""

import math
import random

from string_utils import (
    count_characters,
    convert_to_uppercase
)


# Program 22
# Use math module to find square root, power and factorial

def demonstrate_math_module() -> None:
    """
    Demonstrate functions from the math module.
    """

    try:
        number = int(
            input("Enter a non-negative integer: ")
        )

        exponent = int(
            input("Enter exponent value: ")
        )

        if number < 0:
            print(
                "Square root and factorial "
                "cannot be calculated "
                "for negative numbers."
            )
            return

        print("\nMath Module Operations")

        print(
            f"Square Root of {number} = "
            f"{math.sqrt(number)}"
        )

        print(
            f"{number}^{exponent} = "
            f"{math.pow(number, exponent)}"
        )

        print(
            f"Factorial of {number} = "
            f"{math.factorial(number)}"
        )

    except ValueError:
        print(
            "Invalid input. "
            "Please enter integers only."
        )


# Program 23
# Generate random numbers using random module

def demonstrate_random_module() -> None:
    """
    Demonstrate functions from the random module.
    """

    print("\nRandom Module Operations")

    print(
        f"Random Integer (1-100) = "
        f"{random.randint(1, 100)}"
    )

    print(
        f"Random Floating Point Number = "
        f"{random.random()}"
    )


# Program 24
# Create your own module and import it

def demonstrate_custom_module() -> None:
    """
    Demonstrate custom string utility module.
    """

    text = input("\nEnter a string: ").strip()

    if not text:
        print("Input string cannot be empty.")
        return

    print("\nCustom Module Operations")

    print(
        f"Character Count = "
        f"{count_characters(text)}"
    )

    print(
        f"Uppercase Text = "
        f"{convert_to_uppercase(text)}"
    )


if __name__ == "__main__":

    print(
        "========== Python Modules Assignment =========="
    )

    # Question 22
    demonstrate_math_module()

    # Question 23
    demonstrate_random_module()

    # Question 24
    demonstrate_custom_module()