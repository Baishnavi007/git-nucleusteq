"""
Question 4

Create multiple threads to
simulate file downloading
using time.sleep().
"""

import threading
import time


def download_file(file_name: str) -> None:
    """
    Simulate file downloading.
    """

    print(f"Downloading {file_name}...")

    # Simulate the  download time.
    time.sleep(2)

    print(f"{file_name} is downloaded.")


if __name__ == "__main__":

    file_names = [
        "First.pdf",
        "Second.pdf",
        "Third.pdf"
    ]

    threads = []

    for file_name in file_names:

        
        thread = threading.Thread(
            target=download_file,
            args=(file_name,)
        )

        threads.append(thread)

        # Thread execution started for each file download.
        thread.start()

    # Wait for all threads to complete their execution.
    for thread in threads:
        thread.join()