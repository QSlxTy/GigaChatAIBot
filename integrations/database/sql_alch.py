import sqlalchemy.ext.asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.orm import sessionmaker

from integrations.database.models.generation_style import GenerationStyle
from integrations.database.models.questions import Questions
from integrations.database.models.stories import Stories
from integrations.database.models.story_parts import StoryParts
from integrations.database.models.user import User
from integrations.database.models.user_answers import UserAnswers
from integrations.database.models.user_photos import UserPhotos
from src.config import conf


def get_session_maker(engine: sqlalchemy.ext.asyncio.AsyncEngine) -> sessionmaker:
    return sessionmaker(engine, class_=sqlalchemy.ext.asyncio.AsyncSession, expire_on_commit=False)


async def create_connection() -> sqlalchemy.ext.asyncio.AsyncEngine:
    url = conf.db.build_connection_str()

    engine = _create_async_engine(
        url=url, pool_pre_ping=True)
    return engine


class Database:
    def __init__(
            self,
            session: AsyncSession,
            user: User = None,
            user_answers: UserAnswers = None,
            questions: Questions = None,
            user_photos: UserPhotos = None,
            story_parts: StoryParts = None,
            stories: Stories = None,
            generation_style: GenerationStyle = None

    ):
        self.session = session
        self.user = user or User()
        self.user_answers = user_answers or UserAnswers()
        self.questions = questions or Questions()
        self.user_photos = user_photos or UserPhotos()
        self.story_parts = story_parts or StoryParts()
        self.stories = stories or Stories()
        self.generation_style = generation_style or GenerationStyle()


async def init_models(engine):
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)
        await conn.run_sync(UserAnswers.metadata.create_all)
        await conn.run_sync(Questions.metadata.create_all)
        await conn.run_sync(UserPhotos.metadata.create_all)
        await conn.run_sync(StoryParts.metadata.create_all)
        await conn.run_sync(Stories.metadata.create_all)
        await conn.run_sync(GenerationStyle.metadata.create_all)
