
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.tint import Tint,TintStatus
from sqlalchemy import func, update, delete, and_, or_
from sqlalchemy.orm import joinedload
from app.models.tint import Tint, TintStatus
from typing import List, Optional, Dict, Any

class TintRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, tint: Tint) -> Tint:
        self.db.add(tint)
        await self.db.commit()
        await self.db.refresh(tint)
        return tint

    async def get_by_user(self, user_id: int) -> List[Tint]:
        result = await self.db.execute(
            select(Tint).where(Tint.user_id == user_id).order_by(Tint.created_at.desc())
        )
        return result.scalars().all()
    
    async def get_by_id(self, tint_id: int,load_relationships: bool = False)-> Optional[Tint]:
        # result = await self.db.execute(select(Tint).where(Tint.id == tint_id))
        # return result.scalar_one_or_none()
        query = select(Tint).where(Tint.id == tint_id)
        if load_relationships:
            query = query.options(joinedload(Tint.vehicle), joinedload(Tint.user))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Tint]:
        result = await self.db.execute(
            select(Tint).offset(skip).limit(limit).order_by(Tint.created_at.desc())
        )
        return result.scalars().all()

    async def get_by_vehicle(self, vehicle_id: int) -> List[Tint]:
        result = await self.db.execute(
            select(Tint).where(Tint.vehicle_id == vehicle_id)
        )
        return result.scalars().all()

    async def get_by_user_and_vehicle(self, user_id: int, vehicle_id: int) -> List[Tint]:
        result = await self.db.execute(
            select(Tint).where(
                Tint.user_id == user_id,
                Tint.vehicle_id == vehicle_id
            )
        )
        return result.scalars().all()

    async def delete(self, tint: Tint):
        await self.db.delete(tint)
        await self.db.commit()
        return tint
    
    async def update(self, tint: Tint, updates: dict) -> Tint:
        for key, value in updates.items():
            setattr(tint, key, value)
        self.db.add(tint)
        await self.db.commit()
        await self.db.refresh(tint)
        return tint
    
#   ---- More queries ----
    async def get_by_status(self, status: str, skip: int = 0, limit: int = 50):
        result = await self.db.execute(
            select(Tint)
            .where(Tint.status == status)
            .offset(skip)
            .limit(limit)
            .order_by(Tint.created_at.desc())
        )
        return result.scalars().all()

    async def get_recommended(self, limit: int = 10):
        result = await self.db.execute(
            select(Tint)
            .where(Tint.is_recommended == True)
            .limit(limit)
        )
        return result.scalars().all()

    async def search(
        self,
        brand: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ):
        query = select(Tint)

        filters = []
        if brand:
            filters.append(Tint.film_brand.ilike(f"%{brand}%"))
        if min_price is not None:
            filters.append(Tint.price >= min_price)
        if max_price is not None:
            filters.append(Tint.price <= max_price)
        if status:
            filters.append(Tint.status == status)

        if filters:
            query = query.where(and_(*filters))

        query = query.offset(skip).limit(limit).order_by(Tint.price)
        
        result = await self.db.execute(query)
        return result.scalars().all()

    # ====== Updates ========
    async def update(self, tint: Tint, updates: Dict[str, Any]) -> Tint:
        for key, value in updates.items():
            if hasattr(tint, key):
                setattr(tint, key, value)
        
        await self.db.commit()
        await self.db.refresh(tint)
        return tint

    async def update_status(self, tint_id: int, new_status: TintStatus, approved_by: Optional[int] = None):
        stmt = update(Tint).where(Tint.id == tint_id).values(
            status=new_status.value,
            approved_by=approved_by,
            updated_at=func.now()
        )
        await self.db.execute(stmt)
        await self.db.commit()
        
        return await self.get_by_id(tint_id)

    # ==== Delete =====
    async def delete(self, tint: Tint):
        await self.db.delete(tint)
        await self.db.commit()
        return True