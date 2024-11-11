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
            groups = await session.execute(select(Questions.group).distinct())
            unique_groups = [group[0] for group in groups]
            random_questions = []
            for group in unique_groups:
                random_question = await session.execute(
                    select(Questions).where(Questions.group == group).order_by(func.random()).limit(1)
                )
                random_questions.append(random_question.scalar_one_or_none())

            return random_questions
