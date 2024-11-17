import os
import time

from aiogram import types, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from sqlalchemy.orm import sessionmaker

from keyboards.user.user_keyboard import choose_style_kb


async def start_skip_photo(call: types.CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    await call.message.answer(
        text="<b>Отлично! Сейчас я соберу твою историю и начну рисовать твою персональную комикс-историю. "
             "Кстати, а в каком стиле мне ее сделать?</b>",
        reply_markup=await choose_style_kb()
    )


def register_handler(dp: Dispatcher):
    dp.callback_query.register(start_skip_photo, F.data == 'skip_photo')
