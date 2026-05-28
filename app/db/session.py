from sqlalchemy.ext.asyncio import AsyncSession,async_sessionmaker
# from app.config.database import AsyncSessionLocal
from app.config.database import engine

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session