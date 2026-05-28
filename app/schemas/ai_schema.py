from pydantic import BaseModel
from typing import Optional, List

class TintRecommendationRequest(BaseModel):
    vehicle_make: str
    vehicle_model: str
    year: int
    preferred_tint: Optional[str] = None

class TintRecommendationResponse(BaseModel):
    recommendations: List[dict]
    best_match: dict
    preview_url: Optional[str] = None

class Config:
        from_attributes = True
        