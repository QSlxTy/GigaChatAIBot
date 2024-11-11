import os

from aiogram import types, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from bot_start import bot
from integrations.database.models.user_photos import create_photo_db
from utils.gigachat_api import gigachat_generate_text
from utils.s3 import s3
from utils.states.user import FSMQuestions


async def process_answer(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    data = await state.get_data()
    if not os.path.exists(f'files/{message.from_user.id}/'):
        os.makedirs(f'files/{message.from_user.id}/')

    if message.photo:
        await message.delete()
        await bot.download(message.photo[-1].file_id, f'files/{message.from_user.id}/{message.photo[-1].file_id}.jpg')
        await s3.start_bucket(
            f'files/{message.from_user.id}/{message.photo[-1].file_id}.jpg', message.photo[-1].file_id
        )
        await create_photo_db(message.from_user.id, message.photo[-1].file_id, session_maker)
    else:
        for file in message.album:
            await file.delete()
            await bot.download(
                file.photo[-1].file_id, f'files/{message.from_user.id}/{file.photo[-1].file_id}.jpg'
            )
            await s3.start_bucket(
                f'files/{message.from_user.id}/{file.photo[-1].file_id}.jpg', file.photo[-1].file_id
            )
            await create_photo_db(message.from_user.id, file.photo[-1].file_id, session_maker)

    try:
        msg = await data['msg'].edit_text(
            text="Отлично! Сейчас я соберу твою историю и начну рисовать твою персональную комикс-историю.")
    except (KeyError, TelegramBadRequest):
        msg = await message.answer(
            text="Отлично! Сейчас я соберу твою историю и начну рисовать твою персональную комикс-историю.")
    await state.update_data(msg=msg)
    await gigachat_generate_text(data['answers_list'])

def register_handler(dp: Dispatcher):
    dp.message.register(process_answer, F.content_type == 'photo', FSMQuestions.wait_photo)
