from logging import getLogger

from sqlalchemy.orm import Session

class BaseRepository():
    """Base class for all repositories"""

    def __init__(self, session: Session):
        self.db = session
        self.logger = getLogger(__name__)
