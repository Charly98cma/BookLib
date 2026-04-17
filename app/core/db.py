from typing import Generator, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from core.config import settings

from models.authors_model import Author
from models.books_models import Book
from models.genres_model import Genre
from models.publishers_model import Publisher
# from models.userbookprogress_model import UserBookProgress
from models.users_model import User

# Database URL composed of user-defined env vars to use user PostgreSQL
DATABASE_URL = (
    "postgresql+psycopg://{user}:{passwd}@{host}:{port}/{dbname}".format(
        user    = settings.POSTGRES_USER,
        passwd  = settings.POSTGRES_PASSWORD,
        host    = settings.POSTGRES_HOST,
        port    = settings.POSTGRES_PORT,
        dbname  = settings.POSTGRES_DB
    )
)

# Create async connection/engine to the database
engine = create_engine(DATABASE_URL, echo=settings.DEBUG_SQL)

# Session factory
SessionFactory = sessionmaker(bind=engine)

def get_db() -> Generator[Session, Any, None]:
    with SessionFactory() as session:
        try:
            yield session
        except:
            session.rollback()
            raise
        else:
            session.commit()

def init_tables() -> None:
    # User.metadata.drop_all(bind=engine)
    User.metadata.create_all(bind=engine)
    # Author.metadata.drop_all(bind=engine)
    Author.metadata.create_all(bind=engine)
    # Book.metadata.drop_all(bind=engine)
    Book.metadata.create_all(bind=engine)
    # Genre.metadata.drop_all(bind=engine)
    Genre.metadata.create_all(bind=engine)
    # Publisher.metadata.drop_all(bind=engine)
    Publisher.metadata.create_all(bind=engine)
