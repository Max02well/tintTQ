from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.services.user_service import UserService
from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserProfileResponse
)
from app.utils.jwt import get_current_user, get_current_admin_user

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Create a new user")
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.create_user(user_data)


@router.get("/me", response_model=UserProfileResponse, summary="Get current user's profile")
async def get_current_user_profile(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = UserService(db)
    user = await service.get_user_by_id(current_user.id)
    
    # Add counts (optional enhancement)
    return {
        **user.__dict__,
        "total_vehicles": len(user.vehicles) if user.vehicles else 0,
        "total_tints": len(user.tints) if user.tints else 0,
        "total_bookings": len(user.bookings) if user.bookings else 0,
    }


@router.get("/{user_id}", response_model=UserResponse, summary="Get a user by ID")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_admin_user)  # Admin only
):
    service = UserService(db)
    return await service.get_user_by_id(user_id)


@router.get("/", response_model=List[UserResponse], summary="Get all users")
async def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    service = UserService(db)
    return await service.get_all_users(skip, limit)


@router.put("/{user_id}", response_model=UserResponse, summary="Update a user by ID")
async def update_user(
    user_id: int,
    updates: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = UserService(db)
    return await service.update_user(user_id, updates, current_user.id)