from app.repositories.tint_repository import TintRepository
from app.schemas.tint_schema import TintCreate
from app.models.tint import Tint

class TintService:
    def __init__(self, db):
        self.repo = TintRepository(db)

    async def create_tint(self, tint_data: TintCreate, user_id: int):
        tint = Tint(**tint_data.model_dump(), user_id=user_id)
        return await self.repo.create(tint)