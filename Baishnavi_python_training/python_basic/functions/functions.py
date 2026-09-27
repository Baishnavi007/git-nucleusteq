"""
Functions
"""

# Program 17. Write a function to calculate square of a number.


def calculate_square(number: float) -> float:
    """
    Calculate square of a number.
    """
    return number ** 2


if __name__ == "__main__":

    print("\n--- Square of a Number ---")

    number = float(input("Enter a number: "))

    print(
        f"Square: "
        f"{calculate_square(number)}"
    )


# Program 18. Write a function to check palindrome (number and string).


def is_number_palindrome(number: int) -> bool:
    """
    Check whether a number is palindrome.
    """
    original_number = number
    reversed_number = 0

    while number > 0:
        digit = number % 10
        reversed_number = (
                                  reversed_number * 10
                          ) + digit
        number //= 10

    return (
            original_number
            == reversed_number
    )


def is_string_palindrome(
        text: str
) -> bool:
    """
    Check whether a string is palindrome.
    """
    text = text.lower()
    text = text.replace(" ", "")

    return text == text[::-1]


if __name__ == "__main__":

    print(
        "\n--- Number Palindrome "
        "Checker ---"
    )

    palindrome_number = int(
        input("Enter a number: ")
    )

    if is_number_palindrome(
            palindrome_number
    ):
        print(
            f"{palindrome_number} "
            f"is a palindrome number."
        )
    else:
        print(
            f"{palindrome_number} "
            f"is not a palindrome number."
        )

    print(
        "\n--- String Palindrome "
        "Checker ---"
    )

    palindrome_text = input(
        "Enter a string: "
    )

    if is_string_palindrome(
            palindrome_text
    ):
        print(
            f"{palindrome_text} "
            f"is a palindrome string."
        )
    else:
        print(
            f"{palindrome_text} "
            f"is not a palindrome string."
        )


# Program 19. Write a function that returns maximum number from a list.


def find_maximum_number(
        numbers: list[int]
) -> int:
    """
    Return the maximum number
    from a list.
    """

    if not numbers:
        raise ValueError(
            "List cannot be empty."
        )

    maximum_number = numbers[0]

    for number in numbers:
        if number > maximum_number:
            maximum_number = number

    return maximum_number


if __name__ == "__main__":

    print(
        "\n--- Maximum Number "
        "from a List ---"
    )

    numbers = [50, 55, 78, 90, 15]

    print(f"Numbers: {numbers}")

    print(
        f"Maximum Number: "
        f"{find_maximum_number(numbers)}"
    )


# Program 20. Write a function using default parameters.


def greet_user(
        user_name: str = "Baishnavi"
) -> str:
    """
    Greet user using a default
    parameter.
    """
    return (
        f"Welcome, {user_name}!"
    )


if __name__ == "__main__":

    print(
        "\n--- Default Parameters ---"
    )

    print(greet_user())
    print(greet_user("Baishnavi"))