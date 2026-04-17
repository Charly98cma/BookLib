import uuid
from typing import Optional, List
from sqlalchemy.sql.expression import select

from models.genres_model import Genre

from repositories._base_repository import BaseRepository

class GenreRepository(BaseRepository):

    # CREATE ###################################################################

    def create_genre(self, genre: Genre) -> Genre:
        self.db.add(genre)
        self.db.flush()
        return genre

    # READ #####################################################################

    def read_genre(self, genre_id: uuid.UUID) -> Optional[Genre]:
        return self.db.get(Genre, genre_id)
    
    def read_all_genres(self) -> List[Genre]:
        stmt = select(Genre)
        return list(self.db.scalars(stmt).all())

    # UPDATE ###################################################################



    # DELETE ###################################################################

    def delete_genre(self, genre: Genre) -> None:
        self.db.delete(genre)

    ############################################################################

    def is_genre_unique(self, genre_name: str) -> bool:
        stmt = select(Genre).where(Genre.name == genre_name)
        result = self.db.scalar(stmt)
        return (result is None)
