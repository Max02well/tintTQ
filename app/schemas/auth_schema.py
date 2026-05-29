# from pydantic import BaseModel, EmailStr
# from typing import Optional

# class Token(BaseModel):
#     access_token: str
#     refresh_token: str
#     token_type: str = "bearer"

# class TokenData(BaseModel):
#     email: Optional[str] = None

# class LoginRequest(BaseModel):
#     email: EmailStr
#     password: str 
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class LoginRequest(BaseModel):
    email: EmailStr    
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None
    phone: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenRefreshRequest(BaseModel):
    refresh_token: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    phone: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True