import asyncio
import logging
import os

from bot_start import dp, bot
from handlers.register_handlers import register_handlers
from integrations.database.sql_alch import create_connection, init_models, get_session_maker
from src.bot.structures.data_structure import TransferData
from src.config import conf
from utils.middlewares.album_md import AlbumMiddleware
from utils.middlewares.database_md import DatabaseMiddleware
from utils.middlewares.register_check_md import RegisterCheck
from utils.middlewares.throttling import RateLimitMiddleware


async def start_bot():
    connection = await create_connection()
    ''' REGISTER MIDDLEWARES and HANDLERS'''
    dp.message.middleware(DatabaseMiddleware())
    dp.message.middleware(RegisterCheck())
    dp.callback_query.middleware(RegisterCheck())
    dp.message.middleware(RateLimitMiddleware())
    dp.callback_query.middleware(RateLimitMiddleware())
    # dp.message.middleware(AlbumMiddleware())
    await register_handlers(dp)
    ''' INITIALIZE DATABASE MODELS and CREATE SESSION '''
    await init_models(connection)
    session_maker = get_session_maker(connection)
    ''' START BOT PENDING and DROP PENDING UPDATES BY DELETING WEBHOOK'''
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True,
                           **TransferData(engine=connection), session_maker=session_maker
                           )


if __name__ == '__main__':
    try:
        logging.basicConfig(level=conf.logging_level)
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        logging.info('Bot stopped')
