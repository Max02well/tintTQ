from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Tint(Base):
    __tablename__ = "tints"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
    tint_level = Column(String, nullable=False)          # e.g., "20%", "35%", "50%"
    film_type = Column(String)                           # Ceramic, Carbon, Dyed
    price = Column(Float, nullable=False)
    status = Column(String, default="pending")           # pending, approved, installed
    preview_url = Column(String, nullable=True)          # AI generated preview
    is_recommended = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    vehicle = relationship("Vehicle", back_populates="tints")
    user = relationship("User", back_populates="tints")
    booking = relationship("Booking", back_populates="tint", uselist=False)