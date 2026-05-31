# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
# from sqlalchemy.orm import relationship
# from app.db.base import Base

# class Vehicle(Base):
#     __tablename__ = "vehicles"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
#     make = Column(String, nullable=False)
#     model = Column(String, nullable=False)
#     year = Column(Integer, nullable=False)
#     color = Column(String)
#     license_plate = Column(String, unique=True, nullable=True)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())

#     user = relationship("User", back_populates="vehicles")
#     tints = relationship("Tint", back_populates="vehicle", cascade="all, delete-orphan")
#     bookings = relationship("Booking", back_populates="vehicle", cascade="all, delete-orphan")
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum


class VehicleType(str, enum.Enum):
    SEDAN = "sedan"
    SUV = "suv"
    HATCHBACK = "hatchback"
    TRUCK = "truck"
    COUPE = "coupe"
    VAN = "van"
    OTHER = "other"


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Core Details
    make = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    color = Column(String(30))
    license_plate = Column(String(20), unique=True, nullable=True)
    vin = Column(String(17), unique=True, nullable=True)  # Vehicle Identification Number
    
    vehicle_type = Column(String(20), default=VehicleType.SEDAN.value)
    fuel_type = Column(String(20))  # petrol, diesel, electric, hybrid
    
    # Extra Info
    features = Column(JSONB, default=dict)  # e.g., {"has_sunroof": true, "has_leather": true}
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="vehicles")
    tints = relationship("Tint", back_populates="vehicle", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="vehicle", cascade="all, delete-orphan")