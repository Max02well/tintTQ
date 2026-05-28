from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BookingCreate(BaseModel):
    tint_id: int
    vehicle_id: int
    booking_date: datetime
    notes: Optional[str] = None

class BookingResponse(BaseModel):
    id: int
    user_id: int
    tint_id: int
    vehicle_id: int
    booking_date: datetime
    status: str
    total_amount: float
    notes: Optional[str]

    class Config:
        from_attributes = True