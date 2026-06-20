"""
Question 3:
Read a number from a file and print its square
using try-except-else-finally.
"""


def read_number_from_file(
    file_path: str
) -> int:
    """
    Read a number from a file.

    Args:
        file_path: Path of the file.

    Returns:
        Integer value read from the file.
    """

    with open(file_path, "r") as file:
        return int(file.read().strip())


if __name__ == "__main__":
    try:
        number = read_number_from_file(
            "test_number.txt"
        )

    except FileNotFoundError:
        print("File does not exist.")

    except ValueError:
        print(
            "File contains invalid data."
        )

    else:
        print(
            f"Square of {number} is "
            f"{number ** 2}"
        )

    finally:
        print(
            "File operation completed."
        )