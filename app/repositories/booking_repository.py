from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, and_, func
from sqlalchemy.orm import joinedload
from typing import List, Optional
from app.models.booking import Booking, BookingStatus


class BookingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, booking: Booking) -> Booking:
        self.db.add(booking)
        await self.db.commit()
        await self.db.refresh(booking)
        return booking

    async def get_by_id(self, booking_id: int, load_relationships: bool = False) -> Optional[Booking]:
        query = select(Booking).where(Booking.id == booking_id)
        if load_relationships:
            query = query.options(
                joinedload(Booking.tint),
                joinedload(Booking.vehicle),
                joinedload(Booking.user)
            )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_reference(self, booking_reference: str) -> Optional[Booking]:
        result = await self.db.execute(
            select(Booking).where(Booking.booking_reference == booking_reference)
        )
        return result.scalar_one_or_none()

    async def get_by_user(self, user_id: int, skip: int = 0, limit: int = 50) -> List[Booking]:
        result = await self.db.execute(
            select(Booking)
            .where(Booking.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(Booking.booking_date.desc())
        )
        return result.scalars().all()

    async def get_by_tint(self, tint_id: int) -> Optional[Booking]:
        result = await self.db.execute(
            select(Booking).where(Booking.tint_id == tint_id)
        )
        return result.scalar_one_or_none()

    async def get_upcoming(self, user_id: Optional[int] = None, skip: int = 0, limit: int = 20) -> List[Booking]:
        query = select(Booking).where(Booking.booking_date >= func.now())
        if user_id:
            query = query.where(Booking.user_id == user_id)
        query = query.offset(skip).limit(limit).order_by(Booking.booking_date.asc())
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update(self, booking: Booking, updates: dict) -> Booking:
        for key, value in updates.items():
            if hasattr(booking, key):
                setattr(booking, key, value)
        await self.db.commit()
        await self.db.refresh(booking)
        return booking

    async def update_status(self, booking_id: int, new_status: BookingStatus, cancellation_reason: Optional[str] = None):
        values = {"status": new_status.value}
        if cancellation_reason:
            values["cancellation_reason"] = cancellation_reason

        stmt = update(Booking).where(Booking.id == booking_id).values(**values)
        await self.db.execute(stmt)
        await self.db.commit()
        return await self.get_by_id(booking_id)

    async def delete(self, booking: Booking):
        await self.db.delete(booking)
        await self.db.commit()
        return True