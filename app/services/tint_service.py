from app.repositories.tint_repository import TintRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from app.schemas.tint_schema import TintCreate, TintUpdate
from app.models.tint import Tint, TintStatus
from fastapi import HTTPException, status
from datetime import datetime, timedelta

class TintService:
    def __init__(self, db : AsyncSession):
        self.repo = TintRepository(db)

    async def create_tint(self, tint_data: TintCreate, user_id: int):
        # if not tint_data.film_brand:
        #     raise HTTPException(status_code=400, detail="Film brand is required")
        # Auto-calculate warranty expiry if not provided
        if tint_data.warranty_months:
            warranty_expiry = datetime.utcnow() + timedelta(days=tint_data.warranty_months * 30)
        else:
            warranty_expiry = None
        tint = Tint(
            **tint_data.model_dump(),
            user_id=user_id,
            warranty_expiry=warranty_expiry,
            status=TintStatus.PENDING.value
            )
        return await self.repo.create(tint)
    
    # ==== Read ========
    async def get_tint_by_id(self, tint_id: int, load_relationships: bool = True) -> Tint:
        tint = await self.repo.get_by_id(tint_id, load_relationships=load_relationships)
        if not tint:
            raise HTTPException(status_code=404, detail="Tint not found")
        return tint

    async def get_user_tints(self, user_id: int) -> List[Tint]:
        return await self.repo.get_by_user(user_id)

    async def get_vehicle_tints(self, vehicle_id: int) -> List[Tint]:
        return await self.repo.get_by_vehicle(vehicle_id)

    async def get_user_vehicle_tints(self, user_id: int, vehicle_id: int) -> List[Tint]:
        return await self.repo.get_by_user_and_vehicle(user_id, vehicle_id)

    async def get_all_tints(self, skip: int = 0, limit: int = 100) -> List[Tint]:
        return await self.repo.get_all(skip=skip, limit=limit)

    async def get_tints_by_status(self, status: str, skip: int = 0, limit: int = 50) -> List[Tint]:
        if status not in [s.value for s in TintStatus]:
            raise HTTPException(status_code=400, detail="Invalid status")
        return await self.repo.get_by_status(status, skip, limit)

    async def get_recommended_tints(self, limit: int = 10) -> List[Tint]:
        return await self.repo.get_recommended(limit)

    async def search_tints(
        self,
        brand: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Tint]:
        return await self.repo.search(brand, min_price, max_price, status, skip, limit)

    # ==== Update ========
    async def update_tint(self, tint_id: int, updates: TintUpdate, current_user_id: int) -> Tint:
        tint = await self.get_tint_by_id(tint_id)

        # Authorization check
        if tint.user_id != current_user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this tint")

        update_dict = updates.model_dump(exclude_unset=True)
        
        return await self.repo.update(tint, update_dict)

    async def update_tint_status(
        self, 
        tint_id: int, 
        new_status: TintStatus, 
        approved_by: int
    ) -> Tint:
        tint = await self.get_tint_by_id(tint_id)
        
        # Business logic: Only allow certain status transitions
        if tint.status == TintStatus.INSTALLED and new_status != TintStatus.EXPIRED:
            raise HTTPException(status_code=400, detail="Cannot change status of installed tint")

        return await self.repo.update_status(tint_id, new_status, approved_by)

    # ==== Delete ====
    async def delete_tint(self, tint_id: int, current_user_id: int) -> bool:
        tint = await self.get_tint_by_id(tint_id)

        # Only owner or admin can delete
        if tint.user_id != current_user_id:
            raise HTTPException(status_code=403, detail="Not authorized")

        # Optional: Prevent deletion of installed tints
        if tint.status == TintStatus.INSTALLED:
            raise HTTPException(status_code=400, detail="Cannot delete installed tint")

        return await self.repo.delete(tint)

    # ==== Business logic =======
    async def recommend_tint(self, tint_id: int, is_recommended: bool):
        """Mark a tint as recommended (for admin use)"""
        tint = await self.get_tint_by_id(tint_id)
        tint.is_recommended = is_recommended
        return await self.repo.update(tint, {"is_recommended": is_recommended})