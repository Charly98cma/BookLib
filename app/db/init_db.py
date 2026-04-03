from db.database import engine

from models.authors_model import Author
from models.books_models import Book
from models.genres_model import Genre
from models.publishers_model import Publisher
# from models.userbookprogress_model import UserBookProgress
from models.users_model import User

async def init_tables():
    # Create all missing tables
    async with engine.begin() as conn:
        # await conn.run_sync(User.metadata.drop_all)
        await conn.run_sync(User.metadata.create_all)
        # await conn.run_sync(Author.metadata.drop_all)
        await conn.run_sync(Author.metadata.create_all)
        # await conn.run_sync(Book.metadata.drop_all)
        await conn.run_sync(Book.metadata.create_all)
        # await conn.run_sync(Genre.metadata.drop_all)
        await conn.run_sync(Genre.metadata.create_all)
        # await conn.run_sync(Publisher.metadata.drop_all)
        await conn.run_sync(Publisher.metadata.create_all)
