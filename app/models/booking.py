from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    tint_id = Column(Integer, ForeignKey("tints.id", ondelete="CASCADE"))
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"))
    
    booking_date = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, default="confirmed")         # confirmed, completed, cancelled
    total_amount = Column(Float, nullable=False)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    tint = relationship("Tint", back_populates="booking")
    vehicle = relationship("Vehicle")