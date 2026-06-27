"""
Category routes
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
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
    admin_only
)

router = APIRouter(
    prefix="/admin/categories",
    tags=["Category Management"]
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
async def create_category(
        category: CategoryCreate,
        current_user=Depends(admin_only)
):
    """
    Create a new category
    """

    try:

        return await CategoryService.create_category(
            category,
            current_user
        )

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.get("")
async def get_all_categories(
        current_user=Depends(admin_only)
):
    """
    Retrieve all categories
    """

    return await CategoryService.get_all_categories()


@router.put("/{category_id}")
async def update_category(
        category_id: str,
        category: CategoryUpdate,
        current_user=Depends(admin_only)
):
    """
    Update an existing category
    """

    try:

        return await CategoryService.update_category(
            category_id,
            category
        )

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.delete("/{category_id}")
async def delete_category(
        category_id: str,
        current_user=Depends(admin_only)
):
    """
    Delete an existing category
    """

    try:

        return await CategoryService.delete_category(
            category_id
        )

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )