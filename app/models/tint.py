from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, func, Text, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import enum

class TintStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    INSTALLED = "installed"
    EXPIRED = "expired"

class Tint(Base):
    __tablename__ = "tints"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Tint Details
    film_brand = Column(String, nullable=False)
    film_series = Column(String, nullable=True)
    # Better than single tint_level
    tint_config = Column(JSONB, nullable=False)  # e.g.,{"front": 35, "rear": 20, "windshield": 70}
    
    tint_level = Column(String, nullable=True)  # e.g., "20%", "35%", "50%"
    film_type = Column(String) 
    # Price
    price = Column(Float, nullable=False)
    currency = Column(String(3), default="KES") # Ceramic, Carbon, Dyed
    # Status
    status = Column(String, default=TintStatus.PENDING.value)
    # pending, approved, installed 
    # Dates
    installation_date = Column(DateTime(timezone=True), nullable=True)
    warranty_months = Column(Integer, default=36)
    warranty_expiry = Column(DateTime(timezone=True), nullable=True)
    # Media & Recommendation
    preview_url = Column(String, nullable=True)
    is_recommended = Column(Boolean, default=False)
    # Metadata
    notes = Column(Text, nullable=True)
    compliance_status = Column(String, default="pending")  # legal, warning, illegal
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    vehicle = relationship("Vehicle", back_populates="tints")
    user = relationship("User", foreign_keys=[user_id], back_populates="tints")
    approver = relationship("User", foreign_keys=[approved_by], back_populates="approved_tints")
    booking = relationship("Booking", back_populates="tint", uselist=False)