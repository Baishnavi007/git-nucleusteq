"""
Question 6
Difference Between Iterator and Generator

Iterator:
- Accesses elements one at a time.
- Uses iter() and next().
- Raises StopIteration when all
  elements are exhausted.

Generator:
- Uses the yield keyword.
- Produces values lazily, one at a time.
- Useful for memory-efficient processing.
"""


def show_iterator_example() -> None:
    """
    Demonstrate how an iterator works.
    """

    student_marks = [78, 85, 92]

    # Create an iterator from the list.
    marks_iterator = iter(student_marks)

    print("Iterator Example:")

    print(next(marks_iterator))
    print(next(marks_iterator))
    print(next(marks_iterator))


def generate_grades():
    """
    Generate grade values one at a time.
    """

    yield "A"
    yield "B"
    yield "C"


if __name__ == "__main__":

    print("\n--- Iterator vs Generator ---\n")

    show_iterator_example()

    print("\nGenerator Example:")

    for grade in generate_grades():
        print(grade)