import os
from collections.abc import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# Database URL composed of user-defined env vars to use user PostgreSQL
DATABASE_URL = (
    "postgresql+asyncpg://{user}:{passwd}@{host}:{port}/{dbname}".format(
        user    = os.getenv('POSTGRES_USER'),
        passwd  = os.getenv('POSTGRES_PASSWORD'),
        host    = os.getenv('POSTGRES_HOST'),
        port    = os.getenv('POSTGRES_PORT'),
        dbname  = os.getenv('POSTGRES_DB')
    )
)

# Create async connection/engine to the database
engine = create_async_engine(DATABASE_URL,
                             echo=(os.getenv("DEBUG")=="True"))

# Session factory to reuse them if possible
factory = async_sessionmaker(engine,
                             expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    # Create a new session from the factory
    async with factory() as session:
        try:
            # Return session and commit changes eventually
            yield session
            await session.commit()
        except SQLAlchemyError as _:
            # If an exception arises, rollback any change made
            await session.rollback()
            raise
