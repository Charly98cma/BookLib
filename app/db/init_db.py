from db.database import engine

from models.users import User

async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)
