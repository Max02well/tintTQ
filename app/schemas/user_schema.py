from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=50)
    middle_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20, pattern=r"^\+?\d{9,15}$")
    full_name: Optional[str] = None  # Will be computed


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    is_superuser: Optional[bool] = None

    model_config = ConfigDict(extra="forbid")


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda v: v.isoformat()}
    )


class UserProfileResponse(UserResponse):
    """Extended response with related data count"""
    total_vehicles: int = 0
    total_tints: int = 0
    total_bookings: int = 0


class UserLogin(BaseModel):
    email: EmailStr
    password: str