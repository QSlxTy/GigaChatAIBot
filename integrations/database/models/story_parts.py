from datetime import datetime

from sqlalchemy import BigInteger, Text, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column

from ..modeles import AbstractModel


class StoryParts(AbstractModel):
    __tablename__ = 'story_parts'

    story_id: Mapped[int] = mapped_column(BigInteger())
    part_number: Mapped[int] = mapped_column(SmallInteger())
    text: Mapped[str] = mapped_column(Text())
    image_url: Mapped[str] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column()
