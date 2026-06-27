"""
Common helper functions
"""

from bson import ObjectId
from bson.errors import InvalidId


def validate_object_id(
        object_id: str
) -> ObjectId:
    """
    Validate and convert a string into MongoDB ObjectId.

    Args:
        object_id:
            MongoDB document ID.

    Returns:
        ObjectId

    Raises:
        ValueError:
            If ObjectId format is invalid.
    """

    try:

        return ObjectId(object_id)

    except InvalidId:

        raise ValueError(
            "Invalid ID format."
        )