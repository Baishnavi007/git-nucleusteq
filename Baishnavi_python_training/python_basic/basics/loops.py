"""
Loops


"""


# Program 12. Print numbers from 1 to 100 using loop.
def print_numbers_from_one_to_hundred() -> None:
    """
    Print numbers from 1 to 100.
    """
    print("\n--- Numbers from 1 to 100 ---")

    for number in range(1, 101):
        print(number)


# Program 13. Print multiplication table of a number.
def print_multiplication_table(
        number: int
) -> None:
    """
    Print multiplication table of a number.
    """

    # Multiplication tables are commonly displayed
    # from 1 to 10
    for multiplier in range(1, 11):
        print(f"{number} x {multiplier} = {number * multiplier}")


# Program 14. Find factorial of a number
def calculate_factorial(
        number: int
) -> int | None:
    """
    Calculate factorial of a number.
    """

    #Handles the edge of negative number
    if number < 0:
        print("Factorial is not defined for negative numbers.")
        return

    factorial = 1

    
    for current_number in range(1, number + 1):
        factorial *= current_number

    return factorial


# Program 15. Reverse a number using loop.
def reverse_number(
        number: int
) -> int | None:
    """
    Reverse a number using loop.
    """
    # Handling the edge case of zero
    if number == 0:
        return 0

    # Handle negative number edge case
    if number < 0:
        print("Please enter a non-negative number.")
        return

    reversed_number = 0

   
    while number > 0:
        digit = number % 10
        reversed_number = (reversed_number * 10) + digit
        number //= 10

    return reversed_number


# Program 16. Check whether a number is prime.
def check_prime_number(
        number: int
) -> bool:
    """
    Check whether a number is prime.
    """
    # Handle numbers less than or equal to 1
    if number <= 1:
        return False

    # A prime number should not be divisible by any number other than 1 and itself
    
    for divisor in range(2, number):
        if number % divisor == 0:
            return False

    return True


if __name__ == "__main__":

    print_numbers_from_one_to_hundred()

    print("\n--- Multiplication Table ---")

    number = int(
        input("Enter a number: ")
    )
    print_multiplication_table(number)

    print("\n--- Factorial Calculator ---")

    factorial_number = int(
        input("Enter a number: ")
    )

    factorial = calculate_factorial(
        factorial_number
    )

    if factorial is not None:
        print(
            f"Factorial of "
            f"{factorial_number} "
            f"is {factorial}."
        )

    print("\n--- Reverse a Number ---")

    reverse_input = int(
        input("Enter a number: ")
    )
    reversed_number = reverse_number(
        reverse_input
    )

    if reversed_number is not None:
        print(
            f"Reversed Number: "
            f"{reversed_number}"
        )

    print("\n--- Prime Number Checker ---")

    prime_input = int(
        input("Enter a number: ")
    )
    if check_prime_number(prime_input):
        print(
            f"{prime_input} "
            f"is a prime number."
        )
    else:
        print(
            f"{prime_input} "
            f"is not a prime number."
        )