from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, func
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import enum

class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

class Booking(Base):
    __tablename__ = "bookings"
    booking_reference = Column(String, unique=True, index=True, nullable=False)  # e.g., BK-20250531-7842

    id = Column(Integer, primary_key=True, index=True)
    # Relationships
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    tint_id = Column(Integer, ForeignKey("tints.id", ondelete="CASCADE"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False)
    
    # Booking Details
    booking_date = Column(DateTime(timezone=True), nullable=False)
    installation_date = Column(DateTime(timezone=True), nullable=True)  # Actual installation

    status = Column(String, default=BookingStatus.PENDING.value)
    payment_status = Column(String, default="pending")  # pending, paid, failed, refunded

    total_amount = Column(Float, nullable=False)
    currency = Column(String(3), default="KES")        # confirmed, completed, cancelled

    # Extra Data
    notes = Column(String, nullable=True)
    cancellation_reason = Column(String, nullable=True)
    booking_metadata = Column(JSONB, default=dict)  # Flexible extra info

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="bookings")
    tint = relationship("Tint", back_populates="booking", uselist=False)
    vehicle = relationship("Vehicle", back_populates="bookings")