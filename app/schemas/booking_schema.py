from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict
from datetime import datetime
from enum import Enum


class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class BookingBase(BaseModel):
    booking_date: datetime
    installation_date: Optional[datetime] = None
    notes: Optional[str] = Field(None, max_length=500)
    total_amount: float = Field(..., gt=0)
    currency: str = Field("KES", min_length=3, max_length=3)


class BookingCreate(BaseModel):
    tint_id: int = Field(..., gt=0)
    vehicle_id: int = Field(..., gt=0)
    booking_date: datetime
    installation_date: Optional[datetime] = None
    notes: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


class BookingUpdate(BaseModel):
    booking_date: Optional[datetime] = None
    installation_date: Optional[datetime] = None
    notes: Optional[str] = None
    status: Optional[BookingStatus] = None
    payment_status: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


class BookingResponse(BaseModel):
    id: int
    booking_reference: str
    user_id: int
    tint_id: int
    vehicle_id: int

    booking_date: datetime
    installation_date: Optional[datetime] = None
    status: BookingStatus
    payment_status: str

    total_amount: float
    currency: str

    notes: Optional[str] = None
    cancellation_reason: Optional[str] = None
    booking_metadata: Dict = Field(default_factory=dict)

    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda v: v.isoformat()}
    )


# Extra schemas
class BookingStatusUpdate(BaseModel):
    status: BookingStatus
    cancellation_reason: Optional[str] = None


class BookingPaymentUpdate(BaseModel):
    payment_status: str