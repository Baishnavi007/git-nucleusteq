"""
Authentication routes
"""

from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.user_schema import (UserRegister, UserLogin, LoginResponse)
from app.services.auth_service import AuthService
from app.security.auth_guard import get_current_user,admin_only,student_only

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserRegister):
    print("Registering user:")
    """
    Create a new user account
    """
    try:
        return await AuthService.register(user)
    
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.post(
    "/login",
    response_model=LoginResponse
)
async def login_user(user: UserLogin):
    """
    Login user
    """
    try:
        return await AuthService.login(user)

    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))

@router.get("/current-user")
async def get_current_user_details(current_user=Depends(get_current_user)):
    """
    Get current user profile
    """
    return current_user

@router.get("/admin/dashboard")
async def admin_dashboard(current_user=Depends(admin_only)):
    """
    Admin dashboard endpoint
    """
    return {
        "message": "Welcome Admin",
         "user":current_user 
    }
   
@router.get("/student/dashboard")
async def student_dashboard(current_user=Depends(student_only)):
    """
     Student dashboard endpoint
    """
    return {
        "message": "Welcome Student",
        "user": current_user
    }