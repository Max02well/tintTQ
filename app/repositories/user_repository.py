from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, and_
from typing import List, Optional
from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        result = await self.db.execute(
            select(User)
            .offset(skip)
            .limit(limit)
            .order_by(User.created_at.desc())
        )
        return result.scalars().all()

    async def update(self, user: User, updates: dict) -> User:
        for key, value in updates.items():
            if hasattr(user, key):
                setattr(user, key, value)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, user: User):
        await self.db.delete(user)
        await self.db.commit()
        return True

    async def search_users(self, query: str, skip: int = 0, limit: int = 20) -> List[User]:
        search = f"%{query}%"
        result = await self.db.execute(
            select(User).where(
                and_(
                    User.is_active == True,
                    (User.email.ilike(search)) |
                    (User.first_name.ilike(search)) |
                    (User.last_name.ilike(search)) |
                    (User.phone.ilike(search))
                )
            ).offset(skip).limit(limit)
        )
        return result.scalars().all()