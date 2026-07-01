"""
Category routes
"""

from fastapi import (
    APIRouter,
    Depends,
    status
)

from app.schemas.category_schema import (
    CategoryCreate,
    CategoryUpdate
)

from app.services.category_service import (
    CategoryService
)

from app.security.auth_guard import (
    get_current_user,
    admin_only
)

from app.utils.loggers import (
    logger
)


router = APIRouter(

    prefix="/categories",

    tags=["Category"]

)


@router.get("")
async def get_all_categories(
        current_user=Depends(
            get_current_user
        )
):
    """
    Retrieve all categories.
    """

    logger.info(
        "Fetch all categories requested by '%s'.",
        current_user["email"]
    )

    return await CategoryService.get_all_categories()


@router.post(

    "",

    status_code=status.HTTP_201_CREATED

)
async def create_category(
        category: CategoryCreate,
        current_user=Depends(
            admin_only
        )
):
    """
    Create a new category.
    """

    logger.info(
        "Create category '%s' requested by '%s'.",
        category.name,
        current_user["email"]
    )

    return await CategoryService.create_category(

        category,

        current_user

    )


@router.put("/{category_id}")
async def update_category(
        category_id: str,
        category: CategoryUpdate,
        current_user=Depends(
            admin_only
        )
):
    """
    Update an existing category.
    """

    logger.info(
        "Update category '%s' requested by '%s'.",
        category_id,
        current_user["email"]
    )

    return await CategoryService.update_category(

        category_id,

        category

    )


@router.delete("/{category_id}")
async def delete_category(
        category_id: str,
        current_user=Depends(
            admin_only
        )
):
    """
    Delete an existing category.
    """

    logger.info(
        "Delete category '%s' requested by '%s'.",
        category_id,
        current_user["email"]
    )

    return await CategoryService.delete_category(

        category_id

    )

@router.get("/{category_id}")
async def get_category_by_id(
        category_id: str,
        current_user=Depends(
            get_current_user
        )
):
    """
    Retrieve a category by its ID.
    """

    logger.info(
        "Fetch category '%s' requested by '%s'.",
        category_id,
        current_user["email"]
    )

    return await CategoryService.get_category_by_id(
        category_id
    )