"""
Data Structures - Dictionary
"""


# Question 32: Create a student dictionary and access values.
def display_student_information(
        student_details: dict[str, str | int]
) -> None:
    """
    Display student information stored
    in a dictionary.
    """

    # Dictionary keys provide direct access
    # to the corresponding student details.

    print(
        f"Name: "
        f"{student_details['name']}"
    )

    print(
        f"Age: "
        f"{student_details['age']}"
    )

    print(
        f"Course: "
        f"{student_details['course']}"
    )


# Question 33: Count frequency of characters in a string using dictionary.
def count_character_frequency(
        input_text: str
) -> dict[str, int]:
    """
    Count the frequency of each character
    present in a string.
    """

    # Converting text to lowercase ensures
    # that uppercase and lowercase letters
    # are treated as the same character.

    input_text = input_text.lower()

    character_frequency = {}

    # Each character is stored as a key,
    # while its occurrence count is stored
    # as the corresponding value.

    for character in input_text:

        character_frequency[character] = (
            character_frequency.get(
                character,
                0
            ) + 1
        )

    return character_frequency


# Question 34: Merge two dictionaries.
def merge_student_records(
        personal_details: dict,
        academic_details: dict
) -> dict:
    """
    Merge two dictionaries into one.
    """

    # The union operator combines
    # key-value pairs from both
    # dictionaries into a new dictionary.

    return (
        personal_details
        |
        academic_details
    )


if __name__ == "__main__":

    print(
        "\nStudent Dictionary"
    )

    student_details = {
        "name": "Baishnavi",
        "age": 22,
        "course": "CSE"
    }

    display_student_information(
        student_details
    )

    print(
        "\nCharacter Frequency"
    )

    input_text = "Computer"

    frequency_result = (
        count_character_frequency(
            input_text
        )
    )

    print(
        f"String: "
        f"{input_text}"
    )

    print(
        f"Frequency: "
        f"{frequency_result}"
    )

    print(
        "\nMerge Dictionaries"
    )

    personal_details = {
        "name": "Baishnavi"
    }

    academic_details = {
        "course": "CSE"
    }

    merged_student_record = (
        merge_student_records(
            personal_details,
            academic_details
        )
    )

    print(
        f"First Dictionary: "
        f"{personal_details}"
    )

    print(
        f"Second Dictionary: "
        f"{academic_details}"
    )

    print(
        f"Merged Dictionary: "
        f"{merged_student_record}"
    )