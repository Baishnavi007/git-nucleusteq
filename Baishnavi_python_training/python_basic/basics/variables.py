"""
Programs demonstrating Python variables,
data types and arithmetic operations.
"""


def display_variable_types() -> None:
    """
    Create variables of different data types
    and display their types.
    """

    student_age: int = 23
    cgpa: float = 8.75
    student_name: str = "Baishnavi"
    is_placed: bool = False

    print("\nVariable Types:")
    print(f"Value: {student_age}, Type: {type(student_age)}")
    print(f"Value: {cgpa}, Type: {type(cgpa)}")
    print(f"Value: {student_name}, Type: {type(student_name)}")
    print(f"Value: {is_placed}, Type: {type(is_placed)}")


def swap_numbers(first_number: int, second_number: int) -> tuple[int, int]:
    """
    Swap two numbers.

    Args:
        first_number: First number
        second_number: Second number

    Returns:
        Tuple containing swapped values
    """

    first_number, second_number = second_number, first_number
    return first_number, second_number


def perform_arithmetic_operations(
    first_number: float,
    second_number: float
) -> None:
    """
    Perform arithmetic operations on two numbers.
    """

    print("\nArithmetic Operations:")
    print(f"Sum = {first_number + second_number}")
    print(f"Difference = {first_number - second_number}")
    print(f"Multiplication = {first_number * second_number}")

    if second_number != 0:
        print(f"Division = {first_number / second_number}")
    else:
        print("Division by zero is not allowed.")


if __name__ == "__main__":

    # Question 4
    display_variable_types()

    # Question 5 & 6
    first_number = int(input("\nEnter first number: "))
    second_number = int(input("Enter second number: "))

    swapped_first, swapped_second = swap_numbers(
        first_number,
        second_number
    )

    print(
        f"\nAfter Swapping: "
        f"{swapped_first}, {swapped_second}"
    )

    perform_arithmetic_operations(
        first_number,
        second_number
    )