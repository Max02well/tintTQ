from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.session import get_db
from app.services.tint_service import TintService
from app.schemas.tint_schema import (
    TintCreate,
    TintUpdate,
    TintResponse,
    TintStatusUpdate,
    TintSearchFilters,
    TintRecommendation
)
from app.utils.jwt import get_current_user, get_current_admin_user 

router = APIRouter()


# ====================== CREATE ======================
@router.post("/", response_model=TintResponse, status_code=status.HTTP_201_CREATED,summary="Create a new tint record")
async def create_tint(
    tint_data: TintCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = TintService(db)
    return await service.create_tint(tint_data, user_id=current_user.id)  # Pass user_id

# ===== Read =======
@router.get("/me", response_model=List[TintResponse], summary="Get all tints for the current user")
async def get_my_tints(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all tints belonging to the logged-in user"""
    service = TintService(db)
    return await service.get_user_tints(current_user.id)


@router.get("/{tint_id}", response_model=TintResponse, summary="Get a tint by its ID")
async def get_tint_by_id(
    tint_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = TintService(db)
    return await service.get_tint_by_id(tint_id, load_relationships=True)


@router.get("/vehicle/{vehicle_id}", response_model=List[TintResponse], summary="Get all tints for a specific vehicle")
async def get_vehicle_tints(
    vehicle_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = TintService(db)
    return await service.get_vehicle_tints(vehicle_id)


@router.get("/user/{user_id}/vehicle/{vehicle_id}", response_model=List[TintResponse], summary="Get all tints for a specific user's vehicle")
async def get_user_vehicle_tints(
    user_id: int,
    vehicle_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)   # Optional: add permission check
):
    service = TintService(db)
    return await service.get_user_vehicle_tints(user_id, vehicle_id)


@router.get("/", response_model=List[TintResponse], summary="Get all tints (Admin only)")
async def get_all_tints(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_admin_user)   # ← Admin only
):
    service = TintService(db)
    return await service.get_all_tints(skip=skip, limit=limit)


@router.get("/status/{status}", response_model=List[TintResponse], summary="Get tints by status (Admin only)")
async def get_tints_by_status(
    status: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    service = TintService(db)
    return await service.get_tints_by_status(status, skip, limit)


@router.get("/recommended", response_model=List[TintResponse], summary="Get recommended tints")
async def get_recommended_tints(
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    service = TintService(db)
    return await service.get_recommended_tints(limit)


# ===== Search & Filter =======
@router.get("/search", response_model=List[TintResponse], summary="Search tints with filters")
async def search_tints(
    filters: TintSearchFilters = Depends(),
    db: AsyncSession = Depends(get_db),
):
    service = TintService(db)
    return await service.search_tints(
        brand=filters.brand,
        min_price=filters.min_price,
        max_price=filters.max_price,
        status=filters.status.value if filters.status else None,
        skip=filters.skip,
        limit=filters.limit,
    )


# ===== Update =======
@router.put("/{tint_id}", response_model=TintResponse, summary="Update a tint")
async def update_tint(
    tint_id: int,
    updates: TintUpdate,
    db: AsyncSession = Depends(get_db),
    current_user= Depends(get_current_user)
):
    service = TintService(db)
    return await service.update_tint(tint_id, updates, current_user.id)


@router.patch("/{tint_id}/status", response_model=TintResponse, summary="Update the status of a tint (Admin only)")
async def update_tint_status(
    tint_id: int,
    status_update: TintStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    service = TintService(db)
    return await service.update_tint_status(
        tint_id, 
        status_update.status, 
        approved_by=status_update.approved_by or current_user.id
    )


@router.patch("/{tint_id}/recommend", response_model=TintResponse, summary="Recommend a tint (Admin only)")
async def recommend_tint(
    tint_id: int,
    recommendation: TintRecommendation,
    db: AsyncSession = Depends(get_db),
    current_user= Depends(get_current_admin_user)
):
    service = TintService(db)
    return await service.recommend_tint(tint_id, recommendation.is_recommended)


# ===== Delete ======
@router.delete("/{tint_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a tint")
async def delete_tint(
    tint_id: int,
    db: AsyncSession = Depends(get_db),
    current_user= Depends(get_current_user)
):
    service = TintService(db)
    await service.delete_tint(tint_id, current_user.id)
    return None