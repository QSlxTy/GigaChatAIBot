from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from keyboards.user.user_keyboard import choose_style_kb


async def start_skip_photo(call: types.CallbackQuery, session_maker: sessionmaker):
    await call.message.answer(
        text='<b>Отлично! Сейчас я соберу твою историю и начну рисовать твою персональную комикс-историю.\n'
             'Кстати, а в каком стиле мне ее сделать?</b>',
        reply_markup=await choose_style_kb(session_maker)
    )


def register_handler(dp: Dispatcher):
    dp.callback_query.register(start_skip_photo, F.data == 'skip_photo')
