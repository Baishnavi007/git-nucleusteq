"""
Introduction to Python

Program:
1. Print welcome message
"""

import sys
# Program 1
def print_welcome_message() -> None:
    """
    Display welcome message for Python training.
    """
    print("Welcome to Python Training")

# Program 2. Display Python version
def display_python_version() -> None:
    """
    Display the installed Python version.
    """
    # Display current Python version
    print(f"Python Version: {sys.version}")


# Program 3. Take user input  and display formatted message
def display_user_information() -> None:
    """
    Take username and age as input
    and display a formatted message.
    """
    user_name = input("Enter your name: ").strip().title()
    user_age = int(input("Enter your age: "))

    # handle invalid age input
    if user_age < 0:
        print("Age cannot be negative.")
    else:
        print(f"Hello {user_name}, "
              f"you are {user_age} years old.")


if __name__ == "__main__":
    print_welcome_message()
    display_python_version()
    display_user_information()