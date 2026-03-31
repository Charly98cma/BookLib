from logging import getLogger

from sqlalchemy.ext.asyncio import AsyncSession

class BaseRepository():
    """Base class for all repositories"""

    def __init__(self, session: AsyncSession):
        self.db = session
        self.logger = getLogger(__name__)
