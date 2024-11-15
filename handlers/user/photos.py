import os
import time

from aiogram import types, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from sqlalchemy.orm import sessionmaker

from bot_start import bot, logger
from integrations.database.models.user_photos import create_photo_db
from utils.gigachat_api import generate_main
from utils.states.user import FSMQuestions


async def process_answer(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    data = await state.get_data()
    if not os.path.exists(f'files/{message.from_user.id}/'):
        os.makedirs(f'files/{message.from_user.id}/')
    if not os.path.exists(f"files/{message.from_user.id}_generated/"):
        os.makedirs(f"files/{message.from_user.id}_generated/")
    if message.photo:
        path_list = [f'files/{message.from_user.id}/{message.photo[-1].file_id}.jpg']
        await message.delete()
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
    try:
        msg = await data['msg'].edit_text(
            text="Отлично! Сейчас я соберу твою историю и начну рисовать твою персональную комикс-историю.")
    except (KeyError, TelegramBadRequest):
        msg = await message.answer(
            text="Отлично! Сейчас я соберу твою историю и начну рисовать твою персональную комикс-историю.")
    # try:
    file_path_list, list_text = await generate_main(data['answers_list'], path_list, message.from_user.id)
    for index, path in enumerate(file_path_list):
        await bot.send_photo(message.from_user.id, photo=FSInputFile(path), caption=list_text[index])
        time.sleep(1)
    # except Exception as _ex:
    #     logger.error(f'Error in generate_main: {_ex}')
    #     msg = await msg.edit_text(
    #         text="Что-то пошло не так. Попробуешь снова? /start"
    #     )
    # finally:
    for file in os.listdir(f'files/{message.from_user.id}'):
        os.remove(f'files/{message.from_user.id}/{file}')
    for file in os.listdir(f'files/{message.from_user.id}_generated'):
        os.remove(f'files/{message.from_user.id}/generated/{file}')

    await state.update_data(msg=msg)


def register_handler(dp: Dispatcher):
    dp.message.register(process_answer, F.content_type == 'photo', FSMQuestions.wait_photo)
