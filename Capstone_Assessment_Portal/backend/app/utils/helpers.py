"""
Common helper functions
"""

from bson import ObjectId
from bson.errors import InvalidId

from app.exceptions.bad_request_exception import (
    BadRequestException
)


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
        BadRequestException:
            If ObjectId format is invalid.
    """

    try:

        return ObjectId(
            object_id
        )

    except InvalidId:

        raise BadRequestException(
            "Invalid ID format."
        )