from datetime import datetime
from sqlalchemy import select, BigInteger, update, Text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column

from ..modeles import AbstractModel


class UserAnswers(AbstractModel):
    __tablename__ = 'user_answers'

    telegram_id: Mapped[int] = mapped_column(BigInteger())
    question: Mapped[str] = mapped_column(Text())
    answer_text: Mapped[str] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column()


async def create_answer_db(telegram_id: int, question_id: str, answer_text: str, session_maker: sessionmaker) -> [UserAnswers, Exception]:
    async with session_maker() as session:
        async with session.begin():
            answer = UserAnswers(
                telegram_id=telegram_id,
                question=question_id,
                answer_text=answer_text,
                created_at=datetime.now()
            )
            try:
                session.add(answer)
                return UserAnswers
            except ProgrammingError as _ex:
                return _ex