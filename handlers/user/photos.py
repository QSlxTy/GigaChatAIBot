import os
from datetime import datetime
from typing import List

from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram_media_group import media_group_handler
from sqlalchemy.orm import sessionmaker

from bot_start import bot
from keyboards.user.user_keyboard import choose_style_kb
from src.config import BotConfig
from utils.s3 import upload_photo_to_yandex_s3, delete_photo_from_yandex_s3
from utils.states.user import FSMQuestions


async def process_answer(messages: List[types.Message], state: FSMContext, session_maker: sessionmaker):
    if len(messages) > 4:
        await messages[0].answer(
            text="Можно загружать не более 4 фото\n"
                 "Заново загрузи 4 фото, которые мне помогут создать образы для твоей истории"
        )
        await state.set_state(FSMQuestions.wait_photo)
        return
    await messages[0].answer_photo(
        photo=FSInputFile(BotConfig.download_photo_path),
        caption="Сохраняю фото..."
    )

    if not os.path.exists(f'files/{messages[0].from_user.id}/'):
        os.makedirs(f'files/{messages[0].from_user.id}/')
    if not os.path.exists(f"files/{messages[0].from_user.id}_generated/"):
        os.makedirs(f"files/{messages[0].from_user.id}_generated/")

    path_list = []
    url_list = []
    date = datetime.now()
    for file in messages:
        url = await upload_photo_to_yandex_s3(bot, file.photo[-1].file_id)
        url_list.append(url)
        path_list.append(f'files/{messages[0].from_user.id}/{file.photo[-1].file_id}{date}.jpg')

    await messages[0].answer(
        text='Отлично! Сейчас я соберу твою историю и начну рисовать твою персональную комикс-историю.'
             'Кстати, какой стиль мне выбрать?',
        reply_markup=await choose_style_kb(session_maker)
    )
    await state.update_data(path_list=path_list, url_list=url_list)


async def process_one_photo(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    print(message)
    await message.answer_photo(
        photo=FSInputFile(BotConfig.download_photo_path),
        caption="Сохраняю фото..."
    )

    if not os.path.exists(f'files/{message.from_user.id}/'):
        os.makedirs(f'files/{message.from_user.id}/')
    if not os.path.exists(f"files/{message.from_user.id}_generated/"):
        os.makedirs(f"files/{message.from_user.id}_generated/")

    date = datetime.now()
    url = await upload_photo_to_yandex_s3(bot, message.photo[-1].file_id)
    name_list = [f'{message.from_user.id}/{message.photo[-1].file_id}{date}.jpg']
    path_list = [f'files/{message.from_user.id}/{message.photo[-1].file_id}{date}.jpg']
    url_list = [url]

    await message.answer(
        text='Отлично! Сейчас я соберу твою историю и начну рисовать твою персональную комикс-историю.'
             'Кстати, какой стиль мне выбрать?',
        reply_markup=await choose_style_kb(session_maker)
    )
    await state.update_data(path_list=path_list, url_list=url_list, name_list=name_list)


@media_group_handler
async def album_handler(messages: List[types.Message], state: FSMContext, session_maker: sessionmaker):
    await process_answer(messages, state, session_maker)


def register_handler(dp: Dispatcher):
    dp.message.register(album_handler, F.content_type == 'photo', F.media_group_id, FSMQuestions.wait_photo)
    dp.message.register(process_one_photo, F.content_type == 'photo', FSMQuestions.wait_photo)
