"""
Global exception handlers for custom exceptions
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.exceptions.bad_request_exception import BadRequestException
from app.exceptions.conflict_exception import ConflictException
from app.exceptions.forbidden_exception import ForbiddenException
from app.exceptions.resource_not_found_exception import ResourceNotFoundException
from app.exceptions.unauthorized_exception import UnauthorizedException
from app.utils.logger import logger


def register_exception_handlers(app: FastAPI):
    """
    Register all custom exception handlers
    """
    
    @app.exception_handler(BadRequestException)
    async def bad_request_exception_handler(request: Request, exception: BadRequestException):
        """
        Handles bad request exceptions
        """
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exception)}
        )


    @app.exception_handler(UnauthorizedException)
    async def unauthorized_exception_handler(request: Request, exception: UnauthorizedException):
        """
        Handles unauthorized exceptions
        """
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(exception)}
        )


    @app.exception_handler(ForbiddenException)
    async def forbidden_exception_handler(request: Request, exception: ForbiddenException):
        """
        Handles forbidden exceptions
        """
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": str(exception)}
        )


    @app.exception_handler(ResourceNotFoundException)
    async def resource_not_found_exception_handler(request: Request, exception: ResourceNotFoundException):
        """
        Handles resource not found exceptions
        """
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exception)}
        )


    @app.exception_handler(ConflictException)
    async def conflict_exception_handler(request: Request, exception: ConflictException):
        """
        Handles conflict exceptions
        """
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exception)}
        )


    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exception: Exception):
        """
        Handles all unexpected exceptions
        """
        logger.exception(f"Unhandled exception: {exception}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"}
        )