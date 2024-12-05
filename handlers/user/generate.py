import os
import time

from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto
from sqlalchemy.orm import sessionmaker

from bot_start import bot
from integrations.database.models.questions import get_random_questions
from keyboards.user.user_keyboard import end_story_kb
from utils.gigachat_api import generate_main
from utils.s3 import s3


async def start_generate(call: types.CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    data = await state.get_data()
    await call.message.answer(
        text='<code>Отлично</code>, начал генерацию истории ⌛️'
    )
    if data.get('path_list'):
        path_list = data['path_list']
    else:
        path_list = []

    # try:
    file_path_list = await generate_main(
        data['answers_list'], path_list, data['url_list'], call.from_user.id, data['style'], call.data.split(':')[1],
        session_maker)
    # except Exception as _ex:
    #     logger.error(f'Generation error {call.from_user.id} --> {_ex}')
    #     await bot.send_message(
    #         chat_id=call.from_user.id,
    #         text='Во время генерации истории возникли проблемы ⚙️\n'
    #              'Попробуйте ещё раз /start\n\n'
    #              '❗️<i>Если проблема продолжается, обратитесь к администратору, он всегда на связи</i>',
    #         reply_markup=await end_story_kb()
    #     )
    #     await state.clear()
    #     questions = await get_random_questions(session_maker)
    #     await state.update_data(questions=questions)
    #     return
    await call.message.answer(
        text='Вот твоя персонализированная история!\n'
             'Приятного просмотра и воспоминаний 😊'
    )

    time.sleep(2)
    await bot.send_media_group(
        chat_id=call.from_user.id,
        media=[
            InputMediaPhoto(type='photo', media=file_path_list[0]),
            InputMediaPhoto(type='photo', media=file_path_list[1]),
            InputMediaPhoto(type='photo', media=file_path_list[2]),
            InputMediaPhoto(type='photo', media=file_path_list[3]),
            InputMediaPhoto(type='photo', media=file_path_list[4])
        ]
    )
    for path in os.listdir(f'files/{call.from_user.id}/'):
        os.remove(f'files/{call.from_user.id}/{path}')
    for path in os.listdir(f'files/{call.from_user.id}_generated/'):
        os.remove(f'files/{call.from_user.id}_generated/{path}')
    for name in data['name_list']:
        await s3.delete_file_bucket(name)
    await bot.send_message(
        chat_id=call.from_user.id,
        text='Спасибо, что подводил итоги года с помощью нашего бота! 🤖\n'
             'Хочешь попробовать еще раз и создать новую историю?\n'
             '<code>Воспоминания</code> – это всегда интересно!',
        reply_markup=await end_story_kb()
    )
    await state.clear()
    questions = await get_random_questions(session_maker)
    await state.update_data(questions=questions)


def register_handler(dp: Dispatcher):
    dp.callback_query.register(start_generate, F.data.startswith('choose_sex'))
