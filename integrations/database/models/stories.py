from datetime import datetime

from sqlalchemy import BigInteger, Text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from ..modeles import AbstractModel


class Stories(AbstractModel):
    __tablename__ = 'stories'

    telegram_id: Mapped[int] = mapped_column(BigInteger())
    story_text: Mapped[str] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column()
    token_used: Mapped[int] = mapped_column(BigInteger())


async def create_stories_db(telegram_id: int, story_text: str, token_used: int, session_maker: sessionmaker) -> \
        [Stories, Exception]:
    async with session_maker() as session:
        async with session.begin():
            story = Stories(
                telegram_id=telegram_id,
                story_text=str(story_text),
                token_used=int(token_used),
                created_at=datetime.now()
            )
            try:
                session.add(story)
                return Stories
            except ProgrammingError as _ex:
                return _ex
