from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TintBase(BaseModel):
    tint_level: str
    film_type: str
    price: float

class TintCreate(TintBase):
    vehicle_id: int

class TintResponse(TintBase):
    id: int
    user_id: int
    vehicle_id: int
    status: str
    preview_url: Optional[str] = None
    is_recommended: bool
    created_at: datetime

    class Config:
        from_attributes = True