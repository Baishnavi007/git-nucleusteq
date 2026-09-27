"""
Object-Oriented Programming (OOP)
"""


# Question 40
# Create a Student class with attributes and display details.

class Student:
    """
    Stores basic information about a student.
    """

    def __init__(
            self,
            name: str,
            age: int,
            course: str
    ):
        self.name = name
        self.age = age
        self.course = course

    def display_details(self) -> None:
        """
        Display student information.
        """

        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Course: {self.course}")


# Question 41
# Create a Car class with a constructor.

class Car:
    """
    Represents a car with its
    brand and model details.
    """

    def __init__(
            self,
            brand: str,
            model: str
    ):
        self.brand = brand
        self.model = model

    def display_car_details(self) -> None:
        """
        Display car information.
        """

        print(f"Brand: {self.brand}")
        print(f"Model: {self.model}")


# Question 42
# Implement inheritance using Person and Employee class.

class Person:
    """
    Base class containing
    common person information.
    """

    def __init__(
            self,
            name: str
    ):
        self.name = name


class Employee(Person):
    """
    Employee inherits properties
    from the Person class and
    adds employee-specific details.
    """

    def __init__(
            self,
            name: str,
            employee_id: int
    ):

        # Reuse the initialization
        # logic already available
        # in the parent class.

        super().__init__(name)

        self.employee_id = employee_id

    def display_employee_details(self) -> None:
        """
        Display employee information.
        """

        print(f"Name: {self.name}")
        print(
            f"Employee ID: "
            f"{self.employee_id}"
        )


# Question 43
# Implement encapsulation using private variables.

class Bank:
    """
    Represents a bank account
    with a private balance.
    """

    def __init__(
            self,
            balance: float
    ):

        # Double underscore makes the
        # balance attribute private and
        # restricts direct access from
        # outside the class.

        self.__balance = balance

    def deposit(
            self,
            amount: float
    ) -> None:
        """
        Add money to the account.
        """

        self.__balance += amount

    def get_balance(self) -> float:
        """
        Return current account balance.
        """

        return self.__balance


# Question 44
# Demonstrate polymorphism using
# different classes with the same method.

class Dog:
    """
    Represents a dog.
    """

    def make_sound(self) -> None:

        print("Bark")


class Cat:
    """
    Represents a cat.
    """

    def make_sound(self) -> None:

        print("Meow")


if __name__ == "__main__":

    print(
        "\nQuestion 40"
    )

    student_details = Student(
        "Baishnavi",
        23,
        "CSE"
    )

    student_details.display_details()

    print(
        "\nQuestion 41"
    )

    car_information = Car(
        "Hyundai",
        "Creta"
    )

    car_information.display_car_details()

    print(
        "\nQuestion 42"
    )

    employee_details = Employee(
        "Baishnavi",
        101
    )

    employee_details.display_employee_details()

    print(
        "\nQuestion 43"
    )

    user_bank_account = Bank(
        1000
    )

    user_bank_account.deposit(
        500
    )

    print(
        f"Balance: "
        f"{user_bank_account.get_balance()}"
    )

    print(
        "\nQuestion 44"
    )

    animal_objects = [
        Dog(),
        Cat()
    ]

    # Both objects respond to the
    # same method call differently,
    # demonstrating polymorphism.

    for animal_object in animal_objects:

        animal_object.make_sound()