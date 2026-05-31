from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict
from datetime import datetime
from enum import Enum


class VehicleType(str, Enum):
    SEDAN = "sedan"
    SUV = "suv"
    HATCHBACK = "hatchback"
    TRUCK = "truck"
    COUPE = "coupe"
    VAN = "van"
    OTHER = "other"


class VehicleBase(BaseModel):
    make: str = Field(..., max_length=50)
    model: str = Field(..., max_length=50)
    year: int = Field(..., ge=1900, le=2030)
    color: Optional[str] = Field(None, max_length=30)
    license_plate: Optional[str] = Field(None, max_length=20)
    vin: Optional[str] = Field(None, max_length=17)
    vehicle_type: VehicleType = VehicleType.SEDAN
    fuel_type: Optional[str] = Field(None, max_length=20)
    features: Dict = Field(default_factory=dict)


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    color: Optional[str] = None
    license_plate: Optional[str] = None
    vin: Optional[str] = None
    vehicle_type: Optional[VehicleType] = None
    fuel_type: Optional[str] = None
    features: Optional[Dict] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(extra="forbid")


class VehicleResponse(VehicleBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda v: v.isoformat()}
    )


class VehicleWithStats(VehicleResponse):
    """Extended response with tint/booking count"""
    total_tints: int = 0
    total_bookings: int = 0