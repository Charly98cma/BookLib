from db.database import engine

from models.users_model import User

async def init_tables():
    # Create all missing tables
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)
