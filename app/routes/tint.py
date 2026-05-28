from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.tint_service import TintService
from app.schemas.tint_schema import TintCreate, TintResponse
# from app.utils.jwt import get_current_user

router = APIRouter()

@router.post("/", response_model=TintResponse)
async def create_tint(tint_data: TintCreate, db: AsyncSession = Depends(get_db), 
                    #   current_user = Depends(get_current_user)
                      ):
    service = TintService(db)
    return await service.create_tint(tint_data
                                    #  , current_user.id
                                     )