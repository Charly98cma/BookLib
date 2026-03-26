import os
from collections.abc import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

DATABASE_URL = (
    "postgresql+asyncpg://{user}:{passwd}@{host}:{port}/{dbname}".format(
        user    = os.getenv('POSTGRES_USER'),
        passwd  = os.getenv('POSTGRES_PASSWORD'),
        host    = os.getenv('POSTGRES_HOST'),
        port    = os.getenv('POSTGRES_PORT'),
        dbname  = os.getenv('POSTGRES_DB')
    )
)

engine = create_async_engine(DATABASE_URL,
                             echo=(os.getenv("DEBUG")=="True"))

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
