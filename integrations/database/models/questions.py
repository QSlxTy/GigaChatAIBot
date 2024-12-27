from sqlalchemy import Text
from sqlalchemy import select, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import sessionmaker

from ..modeles import AbstractModel


class Questions(AbstractModel):
    __tablename__ = 'questions'

    group: Mapped[str] = mapped_column(Text)
    text: Mapped[str] = mapped_column(Text)


async def get_random_questions(session_maker: sessionmaker) -> list:
    async with session_maker() as session:
        async with session.begin():
            random_questions_query = select(Questions).where(Questions.group != 'end').order_by(func.random()).limit(5)
            random_questions = await session.execute(random_questions_query)
            return random_questions.scalars().all()


async def get_end_questions(session_maker: sessionmaker) -> Questions:
    async with session_maker() as session:
        async with session.begin():
            response = await session.execute(select(Questions).where(Questions.group == 'end'))
            response = response.scalars().one()
            return response.text
