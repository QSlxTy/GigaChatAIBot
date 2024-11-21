from sqlalchemy import Text, select
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from ..modeles import AbstractModel


class GenerationStyle(AbstractModel):
    __tablename__ = 'generation_style'

    style: Mapped[str] = mapped_column(Text())
    text: Mapped[str] = mapped_column(Text())


async def get_style_db(style: int, session_maker: sessionmaker) -> GenerationStyle:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(GenerationStyle).where(GenerationStyle.style == style))
            return result.scalars().one().text


async def get_all_style_db(session_maker: sessionmaker) -> [GenerationStyle]:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(GenerationStyle))
            return result.scalars().all()
