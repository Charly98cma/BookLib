import uuid
from typing import Optional,  Sequence
from sqlalchemy.sql.expression import select
from pydantic import EmailStr

from models.users_model import User

from repositories._base_repository import BaseRepository

class UserRepository(BaseRepository):

    # CREATE ###################################################################

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.flush()
        return user

    # READ #####################################################################

    def read_user(self, user_id: uuid.UUID) -> Optional[User]:
        return self.db.get(User, user_id)

    def read_all_users(self) -> Sequence[User]:
        stmt = select(User)
        return self.db.scalars(stmt).all()
    
    def read_user_by_username(self, username: str) -> Optional[User]:
        stmt = select(User).where(User.username == username)
        return self.db.scalar(stmt)

    def is_username_unique(self, username: str) -> bool:
        user_db = self.read_user_by_username(username)
        return (user_db is None)

    def is_email_unique(self, email: EmailStr) -> bool:
        stmt = select(User).where(User.email == email)
        user_db = self.db.scalar(stmt)
        return (user_db is None)

    # UPDATE ###################################################################



    # DELETE ###################################################################
    
    def delete_user(self, user: User) -> None:
        self.db.delete(user)
