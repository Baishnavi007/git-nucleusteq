"""
Programs demonstrating conditional statements.
"""

#Program 7. Check whether a number is even or odd
def check_even_or_odd(number: int) -> None:
    """
    Check whether a number is even or odd.
    """

    if number % 2 == 0:
        print(f"{number} is Even")
    else:
        print(f"{number} is Odd")


#Program 8. Check whether a number is positive, negative or zero
def check_number_sign(number: int) -> None:
    """
    Check whether a number is positive,
    negative or zero.
    """

    if number > 0:
        print(f"{number} is Positive")
    elif number < 0:
        print(f"{number} is Negative")
    else:
        print("Number is Zero")


#Program 9. Find the largest among three numbers
def find_largest_number(
    first_number: int,
    second_number: int,
    third_number: int
) -> None:
    """
    Find the largest among three numbers.
    """

    largest_number = max(
        first_number,
        second_number,
        third_number
    )

    print(f"Largest Number = {largest_number}")


#Program 10. Calculate grade based on marks
def calculate_grade(marks: float) -> None:
    """
    Calculate grade based on marks.
    """

    if marks >= 90:
        grade = "A"
    elif marks >= 75:
        grade = "B"
    elif marks >= 50:
        grade = "C"
    else:
        grade = "Fail"

    print(f"Grade = {grade}")


#Program 11. Check whether a year is a leap year
def check_leap_year(year: int) -> None:
    """
    Check whether a year is a leap year.
    """

    if (year % 400 == 0) or (
        year % 4 == 0 and year % 100 != 0
    ):
        print(f"{year} is a Leap Year")
    else:
        print(f"{year} is Not a Leap Year")


if __name__ == "__main__":

    # Question 7
    number = int(input("Enter a number: "))
    check_even_or_odd(number)

    print()

    # Question 8
    number = int(input("Enter another number: "))
    check_number_sign(number)

    print()

    # Question 9
    first_number = int(input("Enter first number: "))
    second_number = int(input("Enter second number: "))
    third_number = int(input("Enter third number: "))

    find_largest_number(
        first_number,
        second_number,
        third_number
    )

    print()

    # Question 10
    marks = float(input("Enter marks: "))
    calculate_grade(marks)

    print()

    # Question 11
    year = int(input("Enter year: "))
    check_leap_year(year)