"""
Programs demonstrating List operations.
"""


# Program 25
# Create a list of 10 numbers and find sum, max,
# sort it, and remove duplicates.

def list_operations(numbers: list[int]) -> None:
    """
    Perform basic list operations.
    """

    if not numbers:
        print("List cannot be empty.")
        return

    print("\nOriginal List:")
    print(numbers)

    print(f"\nSum = {sum(numbers)}")
    print(f"Maximum Number = {max(numbers)}")
    print(f"Sorted List = {sorted(numbers)}")

    unique_numbers = list(set(numbers))

    print(
        f"List After Removing Duplicates = "
        f"{unique_numbers}"
    )


# Program 26
# Count even and odd numbers in a list.

def count_even_odd(numbers: list[int]) -> None:
    """
    Count even and odd numbers.
    """

    even_count = 0
    odd_count = 0

    for number in numbers:

        if number % 2 == 0:
            even_count += 1
        else:
            odd_count += 1

    print(f"\nEven Numbers Count = {even_count}")
    print(f"Odd Numbers Count = {odd_count}")


# Program 27
# Reverse a list without using reverse().

def reverse_list(numbers: list[int]) -> None:
    """
    Reverse a list.
    """

    reversed_list = numbers[::-1]

    print(
        f"\nReversed List = "
        f"{reversed_list}"
    )


if __name__ == "__main__":

    try:

        numbers = []

        print(
            "Enter 10 integer values:"
        )

        for index in range(10):

            number = int(
                input(
                    f"Enter Number "
                    f"{index + 1}: "
                )
            )

            numbers.append(number)

        # Question 25
        list_operations(numbers)

        # Question 26
        count_even_odd(numbers)

        # Question 27
        reverse_list(numbers)

    except ValueError:

        print(
            "Invalid Input. "
            "Please enter integers only."
        )