import os
import time

from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto, FSInputFile
from sqlalchemy.orm import sessionmaker

from bot_start import bot, logger
from integrations.database.models.questions import get_random_questions
from keyboards.user.user_keyboard import end_story_kb
from src.config import BotConfig
from utils.gigachat_api import generate_main
from utils.s3 import delete_photo_from_yandex_s3


async def start_generate(call: types.CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    data = await state.get_data()
    await call.message.answer_photo(
        photo=FSInputFile(BotConfig.start_generation_photo_path),
        caption='<code>Отлично</code>, начал генерацию истории ⌛️\n\n'
                'Это может занять до <code>15 минут</code>, но обычно я справляюсь быстрее. Пришлю результат в чат'
    )
    if data.get('path_list'):
        path_list = data['path_list']
    else:
        path_list = []
    try:
        file_path_list = await generate_main(
            data['answers_list'], path_list, data['url_list'], call.from_user.id, data['style'], call.data.split(':')[1],
            session_maker
        )
    except Exception as _ex:
        logger.error(f'Generation error {call.from_user.id} --> {_ex}')
        await bot.send_message(
            chat_id=call.from_user.id,
            text='Во время генерации истории возникли проблемы ⚙️\n'
                 'Попробуйте ещё раз /start\n\n'
                 '❗️<i>Если проблема продолжается, обратитесь к администратору, он всегда на связи</i>',
            reply_markup=await end_story_kb()
        )
        await state.clear()
        questions = await get_random_questions(session_maker)
        await state.update_data(questions=questions)
        return
    await call.message.answer(
        text='Вот ваша личная история! Приятного просмотра и воспоминаний 😊'
    )

    time.sleep(2)
    await bot.send_media_group(
        chat_id=call.from_user.id,
        media=[
            InputMediaPhoto(type='photo', media=FSInputFile(file_path_list[0])),
            InputMediaPhoto(type='photo', media=FSInputFile(file_path_list[1])),
            InputMediaPhoto(type='photo', media=FSInputFile(file_path_list[2])),
            InputMediaPhoto(type='photo', media=FSInputFile(file_path_list[3])),
            InputMediaPhoto(type='photo', media=FSInputFile(file_path_list[4]))
        ]
    )
    for url in file_path_list:
        await delete_photo_from_yandex_s3(url.split('https://storage.yandexcloud.net/chatbotgigacht')[-1][1:])
    for path in os.listdir(f'files/{call.from_user.id}/'):
        os.remove(f'files/{call.from_user.id}/{path}')
    for path in os.listdir(f'files/{call.from_user.id}_generated/'):
        os.remove(f'files/{call.from_user.id}_generated/{path}')
    # for name in data['name_list']:
    #     await s3.delete_file_bucket(name)
    await bot.send_message(
        chat_id=call.from_user.id,
        text='Спасибо, что подвели итоги года с помощью нашего бота!\n'
             'Хотите попробовать ещё раз и создать новую яркую историю?\n'
             'Ваши воспоминания — наше вдохновение',
        reply_markup=await end_story_kb()
    )
    await state.clear()
    questions = await get_random_questions(session_maker)
    await state.update_data(questions=questions)


def register_handler(dp: Dispatcher):
    dp.callback_query.register(start_generate, F.data.startswith('choose_sex'))
