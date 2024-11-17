import time

from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from sqlalchemy.orm import sessionmaker

from bot_start import bot
from utils.gigachat_api import generate_main


async def start_generate(call: types.CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    data = await state.get_data()
    await call.message.answer(
        text='Отлично, начал генерацию истории'
    )
    if data.get('path_list'):
        path_list = data['path_list']
    else:
        path_list = []

    file_path_list, list_text = await generate_main(data['answers_list'], path_list, call.from_user.id)
    for index, path in enumerate(file_path_list):
        await bot.send_photo(call.from_user.id, photo=FSInputFile(path), caption=list_text[index])
        time.sleep(1)


def register_handler(dp: Dispatcher):
    dp.callback_query.register(start_generate, F.data.startswith('choose_style'))
