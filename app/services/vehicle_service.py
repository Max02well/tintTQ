from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from fastapi import HTTPException, status

from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.vehicle_schema import VehicleCreate, VehicleUpdate
from app.models.vehicle import Vehicle


class VehicleService:
    def __init__(self, db: AsyncSession):
        self.repo = VehicleRepository(db)

    async def create_vehicle(self, vehicle_data: VehicleCreate, user_id: int) -> Vehicle:
        # Check for duplicate license plate
        if vehicle_data.license_plate:
            existing = await self.repo.get_by_license_plate(vehicle_data.license_plate)
            if existing:
                raise HTTPException(status_code=400, detail="Vehicle with this license plate already exists")

        vehicle = Vehicle(**vehicle_data.model_dump(), user_id=user_id)
        return await self.repo.create(vehicle)

    async def get_vehicle_by_id(self, vehicle_id: int, load_relationships: bool = False) -> Vehicle:
        vehicle = await self.repo.get_by_id(vehicle_id, load_relationships)
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        return vehicle

    async def get_user_vehicles(self, user_id: int, skip: int = 0, limit: int = 50) -> List[Vehicle]:
        return await self.repo.get_by_user(user_id, skip, limit)

    async def update_vehicle(self, vehicle_id: int, updates: VehicleUpdate, current_user_id: int) -> Vehicle:
        vehicle = await self.get_vehicle_by_id(vehicle_id)

        if vehicle.user_id != current_user_id and not vehicle.user.is_admin:  # Admin check
            raise HTTPException(status_code=403, detail="Not authorized to update this vehicle")

        update_dict = updates.model_dump(exclude_unset=True)
        return await self.repo.update(vehicle, update_dict)

    async def delete_vehicle(self, vehicle_id: int, current_user_id: int):
        vehicle = await self.get_vehicle_by_id(vehicle_id)

        if vehicle.user_id != current_user_id and not vehicle.user.is_admin:  # Admin check
            raise HTTPException(status_code=403, detail="Not authorized to delete this vehicle")

        # Optional: Prevent deletion if it has active bookings/tints
        if vehicle.tints or vehicle.bookings:
            raise HTTPException(status_code=400, detail="Cannot delete vehicle with active tints or bookings")

        return await self.repo.delete(vehicle)