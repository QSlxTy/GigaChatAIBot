from datetime import datetime

from sqlalchemy import BigInteger, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..modeles import AbstractModel


class Stories(AbstractModel):
    __tablename__ = 'stories'

    telegram_id: Mapped[int] = mapped_column(BigInteger())
    story_text: Mapped[str] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column()
    token_used: Mapped[int] = mapped_column(BigInteger())
