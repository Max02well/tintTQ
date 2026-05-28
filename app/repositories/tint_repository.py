
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.tint import Tint

class TintRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, tint: Tint):
        self.db.add(tint)
        await self.db.commit()
        await self.db.refresh(tint)
        return tint

    async def get_by_user(self, user_id: int):
        result = await self.db.execute(select(Tint).where(Tint.user_id == user_id))
        return result.scalars().all()