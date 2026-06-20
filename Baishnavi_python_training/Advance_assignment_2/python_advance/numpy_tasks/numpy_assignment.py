"""
Assignment 1: NumPy Basics

This module demonstrates:
1. Array creation
2. Statistical operations
3. Array addition
4. Array multiplication
5. Matrix creation
"""

import numpy as np


def create_array() -> np.ndarray:
    """
    Create a NumPy array.

    Returns:
        np.ndarray: Sample array
    """
    return np.array([10, 20, 30, 40, 50])


def calculate_statistics(numbers: np.ndarray) -> None:
    """
    Display basic statistics of the array.

    Args:
        numbers (np.ndarray): Input array
    """

    print("Mean:", np.mean(numbers))
    print("Maximum:", np.max(numbers))
    print("Minimum:", np.min(numbers))
    print("Sum:", np.sum(numbers))


def perform_array_operations() -> None:
    """
    Perform addition and multiplication on two arrays.
    """

    arr_1 = np.array([1, 2, 3])
    arr_2 = np.array([4, 5, 6])

    print("\nArray 1:", arr_1)
    print("Array 2:", arr_2)

    print("Addition:", arr_1 + arr_2)
    print("Multiplication:", arr_1 * arr_2)


def create_matrix() -> np.ndarray:
    """
    Create a 3x3 matrix.

    Returns:
        np.ndarray: 3x3 matrix
    """

    return np.array(
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
    )


def main() -> None:
    """
    Main function to execute all tasks.
    """

    numbers = create_array()

    print("Original Array:")
    print(numbers)

    print("\nStatistics:")
    calculate_statistics(numbers)

    print("\nArray Operations:")
    perform_array_operations()

    print("\n3x3 Matrix:")
    matrix = create_matrix()
    print(matrix)


if __name__ == "__main__":
    main()