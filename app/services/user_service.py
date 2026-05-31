from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from fastapi import HTTPException, status
import bcrypt

from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.models.user import User


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    def hash_password(self, password: str) -> str:
        # Generate salt and hash password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        # Verify password
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )

    async def create_user(self, user_data: UserCreate) -> User:
        # Check if email exists
        existing = await self.repo.get_by_email(user_data.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        user = User(
            email=user_data.email,
            hashed_password=self.hash_password(user_data.password),
            first_name=user_data.first_name,
            middle_name=user_data.middle_name,
            last_name=user_data.last_name,
            phone=user_data.phone,
            full_name=f"{user_data.first_name or ''} {user_data.middle_name or ''} {user_data.last_name or ''}".strip()
        )

        return await self.repo.create(user)

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await self.repo.get_by_email(email)

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return await self.repo.get_all(skip, limit)

    async def update_user(self, user_id: int, updates: UserUpdate, current_user_id: int) -> User:
        user = await self.get_user_by_id(user_id)

        if user.id != current_user_id and not user.is_admin:
            raise HTTPException(status_code=403, detail="Not authorized")

        update_dict = updates.model_dump(exclude_unset=True)
        return await self.repo.update(user, update_dict)

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = await self.get_user_by_email(email)
        if not user or not self.verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return user