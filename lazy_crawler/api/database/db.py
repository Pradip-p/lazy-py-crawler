from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from lazy_crawler.api.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True, future=True)


from sqlalchemy import text


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all) # For dev only
        await conn.run_sync(SQLModel.metadata.create_all)

        # Ensure is_superuser column exists
        try:
            await conn.execute(
                text(
                    'ALTER TABLE "user" ADD COLUMN IF NOT EXISTS is_superuser BOOLEAN DEFAULT FALSE;'
                )
            )
        except Exception:
            pass  # Ignore if it already exists or if there's another issue


async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
