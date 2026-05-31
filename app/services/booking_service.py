from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from fastapi import HTTPException, status
from datetime import datetime, timedelta

from app.repositories.booking_repository import BookingRepository
from app.schemas.booking_schema import BookingCreate, BookingUpdate, BookingResponse, BookingStatusUpdate
from app.models.booking import Booking, BookingStatus
from app.models.tint import Tint
import uuid


class BookingService:
    def __init__(self, db: AsyncSession):
        self.repo = BookingRepository(db)
        
    async def generate_unique_reference(self) -> str:
        """Generate a truly unique booking reference"""
        while True:
            # Use timestamp with microseconds + random UUID
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
            random_part = uuid.uuid4().hex[:8].upper()
            booking_reference = f"BK-{timestamp}-{random_part}"
            
            # Check if it exists (optional - for extra safety)
            existing = await self.repo.get_by_reference(booking_reference)
            if not existing:
                return booking_reference

    async def create_booking(self, booking_data: BookingCreate, user_id: int) -> Booking:
        # Fetch tint to validate and get price
        # You can inject TintService or query directly
        from app.services.tint_service import TintService
        tint_service = TintService(self.repo.db)
        tint = await tint_service.get_tint_by_id(booking_data.tint_id)

        if tint.user_id != user_id:
            raise HTTPException(status_code=403, detail="You can only book your own tint")
   
        # Auto-generate reference
        # booking_reference = f"BK-{datetime.utcnow().strftime('%Y%m%d')}-{abs(hash(str(user_id) + str(booking_data.tint_id))) % 10000:04d}"
        booking_reference = await self.generate_unique_reference()

        booking = Booking(
            **booking_data.model_dump(), # Ensure ID is None for auto-generation
            user_id=user_id,
            booking_reference=booking_reference,
            total_amount=tint.price,          # Pull from Tint
            currency=tint.currency,
            status=BookingStatus.PENDING.value
        )

        return await self.repo.create(booking)

    async def get_booking_by_id(self, booking_id: int, load_relationships: bool = True):
        booking = await self.repo.get_by_id(booking_id, load_relationships)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        return booking

    async def get_user_bookings(self, user_id: int, skip: int = 0, limit: int = 50):
        return await self.repo.get_by_user(user_id, skip, limit)

    async def get_upcoming_bookings(self, user_id: Optional[int] = None):
        return await self.repo.get_upcoming(user_id)

    async def update_booking(self, booking_id: int, updates: BookingUpdate, current_user_id: int):
        booking = await self.get_booking_by_id(booking_id)

        if booking.user_id != current_user_id:
            raise HTTPException(status_code=403, detail="Not authorized")

        # Prevent updating completed/cancelled bookings
        if booking.status in [BookingStatus.COMPLETED.value, BookingStatus.CANCELLED.value]:
            raise HTTPException(status_code=400, detail="Cannot modify completed or cancelled booking")

        update_dict = updates.model_dump(exclude_unset=True)
        return await self.repo.update(booking, update_dict)

    async def update_booking_status(self, booking_id: int, status_update: BookingStatusUpdate, current_user_id: int):
        # Usually admin or owner
        booking = await self.get_booking_by_id(booking_id)
        if booking.user_id != current_user_id:   # Add admin check if needed
            raise HTTPException(status_code=403, detail="Not authorized")

        return await self.repo.update_status(
            booking_id, 
            status_update.status, 
            status_update.cancellation_reason
        )