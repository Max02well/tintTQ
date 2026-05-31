from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.services.vehicle_service import VehicleService
from app.schemas.vehicle_schema import (
    VehicleCreate,
    VehicleUpdate,
    VehicleResponse,
    VehicleWithStats
)
from app.utils.jwt import get_current_user, get_current_admin_user

router = APIRouter()

# ====================== CREATE ======================
@router.post("/", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    vehicle_data: VehicleCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = VehicleService(db)
    return await service.create_vehicle(vehicle_data, current_user.id)


# ====================== READ ======================
@router.get("/me", response_model=List[VehicleResponse])
async def get_my_vehicles(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = VehicleService(db)
    return await service.get_user_vehicles(current_user.id, skip, limit)


@router.get("/{vehicle_id}", response_model=VehicleWithStats)
async def get_vehicle(
    vehicle_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = VehicleService(db)
    vehicle = await service.get_vehicle_by_id(vehicle_id, load_relationships=True)

    if vehicle.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    return vehicle


@router.get("/", response_model=List[VehicleResponse])
async def get_all_vehicles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_admin_user)  # Admin only
):
    service = VehicleService(db)
    return await service.repo.get_all(skip=skip, limit=limit)


# ====================== UPDATE / DELETE ======================
@router.put("/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(
    vehicle_id: int,
    updates: VehicleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = VehicleService(db)
    return await service.update_vehicle(vehicle_id, updates, current_user.id)


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vehicle(
    vehicle_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = VehicleService(db)
    await service.delete_vehicle(vehicle_id, current_user.id)
    return None