from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from keyboards.user.user_keyboard import choose_style_kb, choose_sex_kb


async def start_skip_photo(call: types.CallbackQuery, session_maker: sessionmaker):
    await call.message.answer(
        text='Отлично! Сейчас я соберу твою историю и начну рисовать твою персональную комикс-историю.\n'
             'Кстати, а в каком стиле мне ее сделать?',
        reply_markup=await choose_style_kb(session_maker)
    )


async def choose_sex(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(
        text='Хорошо. Остался последний штрих. Укажите свой пол, чтобы полностью кастомизировать историю.',
        reply_markup=await choose_sex_kb()
    )
    await state.update_data(style=call.data.split(':')[2])


def register_handler(dp: Dispatcher):
    dp.callback_query.register(start_skip_photo, F.data == 'skip_photo')
    dp.callback_query.register(choose_sex, F.data.startswith('choose_style'))
