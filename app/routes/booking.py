from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.session import get_db
from app.services.booking_service import BookingService
from app.schemas.booking_schema import (
    BookingCreate,
    BookingUpdate,
    BookingResponse,
    BookingStatusUpdate,
    BookingPaymentUpdate
)
from app.utils.jwt import get_current_user, get_current_admin_user

router = APIRouter()


# ====================== CREATE ======================
@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED, summary="Create a new booking for a tint")
async def create_booking(
    booking_data: BookingCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new booking for a tint"""
    service = BookingService(db)
    return await service.create_booking(booking_data, user_id=current_user.id)


# ====================== READ ======================
@router.get("/me", response_model=List[BookingResponse], summary="Get all bookings for the logged-in user")
async def get_my_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all bookings for the logged-in user"""
    service = BookingService(db)
    return await service.get_user_bookings(current_user.id, skip=skip, limit=limit)


@router.get("/upcoming", response_model=List[BookingResponse], summary="Get upcoming bookings for the logged-in user")
async def get_upcoming_bookings(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get upcoming bookings for current user"""
    service = BookingService(db)
    return await service.get_upcoming_bookings(user_id=current_user.id)


@router.get("/{booking_id}", response_model=BookingResponse, summary="Get a specific booking by ID")
async def get_booking_by_id(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get a specific booking by ID"""
    service = BookingService(db)
    booking = await service.get_booking_by_id(booking_id, load_relationships=True)
    
    # Authorization: Only owner or admin can view
    if booking.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to view this booking")
    
    return booking


@router.get("/", response_model=List[BookingResponse], summary="Get all bookings (Admin only)")
async def get_all_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_admin_user)  # Admin only
):
    """Get all bookings (Admin only)"""
    service = BookingService(db)
    # You may need to add a get_all method in repository/service if not present
    return await service.repo.get_all(skip=skip, limit=limit)  # Add this method if needed


# ====================== UPDATE ======================
@router.put("/{booking_id}", response_model=BookingResponse, summary="Update booking details")
async def update_booking(
    booking_id: int,
    updates: BookingUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update booking details"""
    service = BookingService(db)
    return await service.update_booking(booking_id, updates, current_user.id)


@router.patch("/{booking_id}/status", response_model=BookingResponse, summary="Update booking status (e.g., confirm, cancel)")
async def update_booking_status(
    booking_id: int,
    status_update: BookingStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update booking status (e.g., confirm, cancel)"""
    service = BookingService(db)
    return await service.update_booking_status(booking_id, status_update, current_user.id)


@router.patch("/{booking_id}/payment", response_model=BookingResponse, summary="Update payment status (Admin / Webhook)")
async def update_payment_status(
    booking_id: int,
    payment_update: BookingPaymentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_admin_user)  # Usually admin or payment gateway webhook
):
    """Update payment status (Admin / Webhook)"""
    service = BookingService(db)
    booking = await service.get_booking_by_id(booking_id)
    
    # Add logic here if needed
    update_dict = {"payment_status": payment_update.payment_status}
    return await service.repo.update(booking, update_dict)


# ====================== CANCEL ======================
@router.post("/{booking_id}/cancel", response_model=BookingResponse, summary="Cancel a booking")
async def cancel_booking(
    booking_id: int,
    cancellation_reason: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Cancel a booking"""
    service = BookingService(db)
    status_update = BookingStatusUpdate(
        status="cancelled",
        cancellation_reason=cancellation_reason
    )
    return await service.update_booking_status(booking_id, status_update, current_user.id)


# ====================== DELETE ======================
@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a booking (Only if pending)")
async def delete_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete a booking (Only if pending)"""
    service = BookingService(db)
    booking = await service.get_booking_by_id(booking_id)

    if booking.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    if booking.status not in ["pending", "cancelled"]:
        raise HTTPException(status_code=400, detail="Cannot delete confirmed or completed booking")

    await service.repo.delete(booking)
    return None