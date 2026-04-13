import uuid
from typing import Optional, List, Sequence
from sqlalchemy.sql.expression import select

from models.authors_model import Author

from repositories._base_repository import BaseRepository

class AuthorRepository(BaseRepository):

    # CREATE ###################################################################

    def create_author(self, author: Author) -> Author:
        self.db.add(author)
        self.db.flush()
        return author

    # READ #####################################################################

    def read_author(self, author_id: uuid.UUID) -> Optional[Author]:
        return self.db.get(Author, author_id)
    
    def read_authors_by_id(self, author_id_list: List[uuid.UUID]) -> Sequence[Author]:
        stmt = select(Author).where(Author.id.in_(author_id_list))
        return self.db.scalars(stmt).all()

    def read_all_authors(self) -> Sequence[Author]:
        stmt = select(Author)
        return self.db.scalars(stmt).all()

    def is_author_unique(self, author_name: str) -> bool:
        stmt = select(Author).where(Author.name == author_name)
        author_db = self.db.scalar(stmt)
        return (author_db is None)

    # UPDATE ###################################################################



    # DELETE ###################################################################

    def delete_author(self, author: Author) -> None:
        self.db.delete(author)
