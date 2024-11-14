import os

from aiogram import types, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from bot_start import bot
from integrations.database.models.user_photos import create_photo_db
from utils.gigachat_api import generate_main
from utils.states.user import FSMQuestions


async def process_answer(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    data = await state.get_data()
    if not os.path.exists(f'files/{message.from_user.id}/'):
        os.makedirs(f'files/{message.from_user.id}/')

    if message.photo:
        path = [f'files/{message.from_user.id}/{message.photo[-1].file_id}.jpg']
        await message.delete()
        await bot.download(message.photo[-1].file_id, f'files/{message.from_user.id}/{message.photo[-1].file_id}.jpg')
        await create_photo_db(message.from_user.id, message.photo[-1].file_id, session_maker)
    else:
        path = []
        for file in message.album:
            path.append(f'files/{message.from_user.id}/{file.photo[-1].file_id}.jpg')
            await file.delete()
            await bot.download(
                file.photo[-1].file_id, f'files/{message.from_user.id}/{file.photo[-1].file_id}.jpg'
            )

            await create_photo_db(message.from_user.id, file.photo[-1].file_id, session_maker)

    try:
        msg = await data['msg'].edit_text(
            text="Отлично! Сейчас я соберу твою историю и начну рисовать твою персональную комикс-историю.")
    except (KeyError, TelegramBadRequest):
        msg = await message.answer(
            text="Отлично! Сейчас я соберу твою историю и начну рисовать твою персональную комикс-историю.")
    await state.update_data(msg=msg)
    await generate_main(data['answers_list'], message.from_user.id, path)


def register_handler(dp: Dispatcher):
    dp.message.register(process_answer, F.content_type == 'photo', FSMQuestions.wait_photo)
