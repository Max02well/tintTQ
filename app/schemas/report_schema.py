# from pydantic import BaseModel
# from typing import Optional, Dict, Any

# class ReportCreate(BaseModel):
#     tint_id: int
#     issue_type: str
#     description: Optional[str] = None
    
# class ReportResponse(BaseModel):
#     id: int
#     user_id: int
#     tint_id: int
#     issue_type: str
#     description: Optional[str]
#     created_at: str
#     status: str
#     resolution_details: Optional[Dict[str, Any]]
    
# class Config:
#         from_attributes = True
        