from datetime import datetime
from sqlite3 import ProgrammingError

from sqlalchemy import BigInteger, Text
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from ..modeles import AbstractModel


class UserPhotos(AbstractModel):
    __tablename__ = 'user_photos'

    telegram_id: Mapped[int] = mapped_column(BigInteger())
    photo_url: Mapped[str] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column()


async def create_photo_db(telegram_id: int, photo_url: str, session_maker: sessionmaker) -> [UserPhotos, Exception]:
    async with session_maker() as session:
        async with session.begin():
            photo = UserPhotos(
                telegram_id=telegram_id,
                photo_url=photo_url,
                created_at=datetime.now()
            )
            try:
                session.add(photo)
                return UserPhotos
            except ProgrammingError as _ex:
                return _ex