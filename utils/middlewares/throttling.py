from collections.abc import Awaitable, Callable
from typing import Any
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from datetime import datetime, timedelta
from collections import defaultdict

from bot_start import bot


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.limit = 1
        self.period = 1
        self.user_requests = defaultdict(list)

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        now = datetime.now()

        if isinstance(event, Message) and event.media_group_id:
            return await handler(event, data)

        self.user_requests[user_id] = [
            timestamp for timestamp in self.user_requests[user_id]
            if timestamp > now - timedelta(seconds=self.period)
        ]

        if len(self.user_requests[user_id]) >= self.limit:
            await bot.send_message(
                chat_id=user_id,
                text=f'<b>Слишком много запросов. Пожалуйста, подождите.</b>'
            )
            return

        self.user_requests[user_id].append(now)
        return await handler(event, data)