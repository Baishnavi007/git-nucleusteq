"""
File Handling Operations
"""


# Question 35
# Create a file and write your name into it.

def write_name_to_file(
        file_path: str,
        user_information: str
) -> None:
    """
    Create a file and write text into it.
    """

    # Write mode creates a new file if it
    # does not already exist. If the file
    # exists, its previous content is replaced.

    with open(file_path, "w") as output_file:
        output_file.write(
            user_information
        )


# Question 36
# Read a file and count words, lines and characters.

def count_file_contents(
        file_path: str
) -> tuple[int, int, int]:
    """
    Count total lines, words,
    and characters in a file.
    """

    with open(file_path, "r") as input_file:
        file_content = (
            input_file.read()
        )

    # The file content is analyzed to
    # calculate basic statistics.

    total_lines = len(
        file_content.splitlines()
    )

    total_words = len(
        file_content.split()
    )

    total_characters = len(
        file_content
    )

    return (
        total_lines,
        total_words,
        total_characters
    )


# Question 37
# Append data to an existing file.

def append_to_file(
        file_path: str,
        additional_content: str
) -> None:
    """
    Append content to an existing file.
    """

    # Append mode preserves the existing
    # content and adds new content at
    # the end of the file.

    with open(file_path, "a") as output_file:
        output_file.write(
            additional_content
        )


# Question 38
# Copy content from one file to another.

def copy_file_content(
        source_file_path: str,
        destination_file_path: str
) -> None:
    """
    Copy content from one file
    to another.
    """

    # Read content from source file.

    with open(
            source_file_path,
            "r"
    ) as source_file:

        file_content = (
            source_file.read()
        )

    # Write the same content to
    # the destination file.

    with open(
            destination_file_path,
            "w"
    ) as destination_file:

        destination_file.write(
            file_content
        )


# Question 39
# Search a word in a file.

def search_word_in_file(
        file_path: str,
        search_word: str
) -> bool:
    """
    Search for a word in a file.
    """

    with open(file_path, "r") as input_file:

        file_content = (
            input_file.read()
        )

    # Returns True if the given word
    # exists in the file content.

    return (
        search_word
        in
        file_content
    )


if __name__ == "__main__":

    print(
        "\nQuestion 35"
    )

    write_name_to_file(
        "sample.txt",
        "Hello, my name is Baishnavi Singh."
    )

    print(
        "Content written successfully."
    )

    print(
        "\nQuestion 37"
    )

    append_to_file(
        "sample.txt",
        "\nI am learning Python Programming."
    )

    print(
        "Content appended successfully."
    )

    print(
        "\nQuestion 36"
    )

    (
        total_lines,
        total_words,
        total_characters
    ) = count_file_contents(
        "sample.txt"
    )

    print(
        f"Lines: {total_lines}"
    )

    print(
        f"Words: {total_words}"
    )

    print(
        f"Characters: "
        f"{total_characters}"
    )

    print(
        "\nQuestion 38"
    )

    copy_file_content(
        "sample.txt",
        "copy_sample.txt"
    )

    print(
        "File copied successfully."
    )

    print(
        "\nQuestion 39"
    )

    is_word_present = (
        search_word_in_file(
            "sample.txt",
            "Java"
        )
    )

    print(
        f"Word Found: "
        f"{is_word_present}"
    )