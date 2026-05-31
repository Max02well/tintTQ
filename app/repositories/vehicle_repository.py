from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, and_
from sqlalchemy.orm import joinedload
from typing import List, Optional
from app.models.vehicle import Vehicle


class VehicleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, vehicle: Vehicle) -> Vehicle:
        self.db.add(vehicle)
        await self.db.commit()
        await self.db.refresh(vehicle)
        return vehicle

    async def get_by_id(self, vehicle_id: int, load_relationships: bool = False) -> Optional[Vehicle]:
        query = select(Vehicle).where(Vehicle.id == vehicle_id)
        if load_relationships:
            query = query.options(joinedload(Vehicle.tints), joinedload(Vehicle.bookings))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_user(self, user_id: int, skip: int = 0, limit: int = 50) -> List[Vehicle]:
        result = await self.db.execute(
            select(Vehicle)
            .where(Vehicle.user_id == user_id, Vehicle.is_active == True)
            .offset(skip)
            .limit(limit)
            .order_by(Vehicle.created_at.desc())
        )
        return result.scalars().all()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        result = await self.db.execute(
            select(Vehicle).offset(skip).limit(limit).order_by(Vehicle.created_at.desc())
        )
        return result.scalars().all()

    async def update(self, vehicle: Vehicle, updates: dict) -> Vehicle:
        for key, value in updates.items():
            if hasattr(vehicle, key):
                setattr(vehicle, key, value)
        await self.db.commit()
        await self.db.refresh(vehicle)
        return vehicle

    async def delete(self, vehicle: Vehicle):
        await self.db.delete(vehicle)
        await self.db.commit()
        return True

    async def get_by_license_plate(self, license_plate: str) -> Optional[Vehicle]:
        result = await self.db.execute(
            select(Vehicle).where(Vehicle.license_plate == license_plate)
        )
        return result.scalar_one_or_none()