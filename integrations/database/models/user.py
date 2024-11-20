from datetime import datetime
from sqlalchemy import select, BigInteger, update, Text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column

from ..modeles import AbstractModel


class User(AbstractModel):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger(), unique=True)
    agreed: Mapped[bool] = mapped_column(default=False)
    create_at: Mapped[datetime] = mapped_column()
    updated_at: Mapped[datetime] = mapped_column()
    is_admin: Mapped[bool] = mapped_column(default=False)


async def get_user_db(select_by: dict, session_maker: sessionmaker) -> User:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User).filter_by(**select_by)
            )
            return result.scalars().one()


async def create_user_db(user_id: int, session_maker: sessionmaker) -> [User, Exception]:
    async with session_maker() as session:
        async with session.begin():
            user = User(
                telegram_id=user_id,
                create_at=datetime.now(),
                updated_at = datetime.now()
            )
            try:
                session.add(user)
                return User
            except ProgrammingError as _e:
                return _e


async def is_user_exists_db(user_id: int, session_maker: sessionmaker) -> bool:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(select(User).where(User.telegram_id == user_id))
            return bool(sql_res.first())


async def update_user_db(telegram_id: int, data: dict, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            await session.execute(update(User).where(User.telegram_id == telegram_id).values(data))
            await session.commit()


async def get_users_db(session_maker: sessionmaker) -> User:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(User))
            return result.scalars().all()
