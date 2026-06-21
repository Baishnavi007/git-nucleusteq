"""
Question 8:
Handle FileNotFoundError when
trying to open a file.
"""


def read_file(file_name: str) -> None:
    """
    Read and display the contents
    of a file.

    Args:
        file_name: Name of the file.
    """

    with open(
        file_name,
        "r",
        encoding="utf-8"
    ) as file:
        print(file.read())


def main() -> None:
    """
    Execute the program.
    """

    try:
        read_file(
            "sample.txt"
        )

    except FileNotFoundError:
        print(
            "File not found."
        )


if __name__ == "__main__":
    main()