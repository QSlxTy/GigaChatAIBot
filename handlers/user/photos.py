import os
import time

from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from sqlalchemy.orm import sessionmaker

from bot_start import bot
from integrations.database.models.user_photos import create_photo_db
from keyboards.user.user_keyboard import choose_style_kb
from utils.gigachat_api import generate_main
from utils.states.user import FSMQuestions


async def process_answer(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    if not os.path.exists(f'files/{message.from_user.id}/'):
        os.makedirs(f'files/{message.from_user.id}/')
    if not os.path.exists(f"files/{message.from_user.id}_generated/"):
        os.makedirs(f"files/{message.from_user.id}_generated/")
    if message.photo:
        path_list = [f'files/{message.from_user.id}/{message.photo[-1].file_id}.jpg']
        await bot.download(message.photo[-1].file_id, f'files/{message.from_user.id}/{message.photo[-1].file_id}.jpg')
        await create_photo_db(message.from_user.id, message.photo[-1].file_id, session_maker)
    else:
        path_list = []
        print(message.album)
        for file in message.album:
            path_list.append(f'files/{message.from_user.id}/{file.photo[-1].file_id}.jpg')
            await file.delete()
            await bot.download(
                file.photo[-1].file_id, f'files/{message.from_user.id}/{file.photo[-1].file_id}.jpg'
            )
            await create_photo_db(message.from_user.id, file.photo[-1].file_id, session_maker)
        await message.answer(
            text="Отлично! Сейчас я соберу твою историю и начну рисовать твою персональную комикс-историю."
                 "Кстати, какой стиль мне выбрать?",
            reply_markup=await choose_style_kb()
        )
    await state.update_data(path_list=path_list)


def register_handler(dp: Dispatcher):
    dp.message.register(process_answer, F.content_type == 'photo', FSMQuestions.wait_photo)
