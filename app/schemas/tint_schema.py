from pydantic import BaseModel, Field, ConfigDict
from typing import Optional,Dict, Any
from datetime import datetime
from enum import Enum

class TintStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    INSTALLED = "installed"
    EXPIRED = "expired"

class TintBase(BaseModel):
    #Base schema for tint, used for both create and update operations
    # tint_level: str
    # film_type: str
    # price: float
    film_brand: str = Field(..., min_length=2, max_length=50, examples=["3M", "LLumar", "XPEL"])
    film_series: Optional[str] = Field(None, max_length=50, examples=["Ceramic IR", "Prime XR"])
    tint_level: Optional[str] = Field(None, max_length=10, examples=["20%", "35%", "50%"])
    film_type: Optional[str] = Field(None, max_length=30, examples=["Ceramic", "Carbon", "Dyed"])
    
    # Using JSON for flexible window-by-window tint levels
    tint_config: Dict[str, int] = Field(
        ..., 
        examples=[{"front": 35, "rear": 20, "windshield": 70, "roof": 15}]
    )
    
    price: float = Field(..., gt=0)
    currency: str = Field("KES", min_length=3, max_length=3)
    
    warranty_months: Optional[int] = Field(36, ge=12, le=120)
    notes: Optional[str] = Field(None, max_length=500)

class TintCreate(TintBase):
    vehicle_id: int = Field(..., gt=0)
    # Optional fields that can be set during creation
    preview_url: Optional[str] = None
    is_recommended: bool = False
    
    
    # ==================== UPDATE ====================
class TintUpdate(BaseModel):
    """Use for partial updates"""
    film_brand: Optional[str] = None
    film_series: Optional[str] = None
    tint_level: Optional[str] = None
    film_type: Optional[str] = None
    tint_config: Optional[Dict[str, int]] = None
    price: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = None
    warranty_months: Optional[int] = None
    notes: Optional[str] = None
    preview_url: Optional[str] = None
    is_recommended: Optional[bool] = None

    model_config = ConfigDict(extra="forbid")  # Prevent unknown fields

class TintResponse(TintBase):
        id: int
        user_id: int
        vehicle_id: int
        approved_by: Optional[int] = None
        
        film_brand: str
        film_series: Optional[str] = None
        tint_config: Dict[str, int]
        
        price: float
        currency: str
        
        tint_level: Optional[str] = None
        film_type: Optional[str] = None
        
        status: TintStatus    
        installation_date: Optional[datetime] = None
        warranty_months: Optional[int] = None
        warranty_expiry: Optional[datetime] = None
        
        preview_url: Optional[str] = None
        is_recommended: bool = False
        notes: Optional[str] = None
        compliance_status: Optional[str] = None

        created_at: datetime
        updated_at: Optional[datetime] = None

        model_config = ConfigDict(
            from_attributes=True,   # Replaces deprecated orm_mode
            json_encoders={
                datetime: lambda v: v.isoformat()
            }
        )
    
class TintStatusUpdate(BaseModel):
    # """Specifically for updating status (admin use)"""
        status: TintStatus
        approved_by: Optional[int] = None
        
class TintSearchFilters(BaseModel):
    # """For query parameters in search endpoint"""
        brand: Optional[str] = None
        min_price: Optional[float] = None
        max_price: Optional[float] = None
        status: Optional[TintStatus] = None
        skip: int = Field(0, ge=0)
        limit: int = Field(20, ge=1, le=100)


class TintRecommendation(BaseModel):
        # """For marking recommended tints"""
        is_recommended: bool

    # class Config:
    #     from_attributes = True