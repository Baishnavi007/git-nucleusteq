"""
Question 5:
Catch all exceptions and print the error message.
"""


DEFAULT_DIVIDEND = 100


def handle_all_exceptions() -> None:
    """
    Perform a division operation and
    catch any exception that occurs.
    """

    try:
        user_number = int(
            input("Enter a number: ")
        )

        result = (
            DEFAULT_DIVIDEND /
            user_number
        )

        print(
            f"Result: {result}"
        )

    except Exception as error:
        print(
            f"An error occurred: {error}"
        )


def main() -> None:
    """
    Execute the program.
    """

    handle_all_exceptions()


if __name__ == "__main__":
    main()