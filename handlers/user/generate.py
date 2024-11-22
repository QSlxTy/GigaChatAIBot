import os
import time

from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from sqlalchemy.orm import sessionmaker

from bot_start import bot
from integrations.database.models.generation_style import get_style_db
from integrations.database.models.questions import get_random_questions
from keyboards.user.user_keyboard import end_story_kb
from utils.gigachat_api import generate_main


async def start_generate(call: types.CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    data = await state.get_data()
    await call.message.answer(
        text='<b><code>Отлично</code>, начал генерацию истории</b>'
    )
    if data.get('path_list'):
        path_list = data['path_list']
    else:
        path_list = []
    file_path_list, list_text = await generate_main(
        data['answers_list'], path_list, call.from_user.id, call.data.split(':')[2], session_maker)
    await bot.send_message(
        chat_id=call.from_user.id,
        text='<b>Вот твоя персонализированная история!\n'
             'Приятного просмотра и воспоминаний 😊</b>'
    )
    time.sleep(2)
    for index, path in enumerate(file_path_list):
        await bot.send_photo(
            chat_id=call.from_user.id,
            photo=FSInputFile(path),
            caption=f'<b>{list_text[index]}</b>'
        )
        os.remove(path)
    for path in os.listdir(f'files/{call.from_user.id}'):
        os.remove(f'files/{call.from_user.id}/{path}')
    await bot.send_message(
        chat_id=call.from_user.id,
        text='<b>Спасибо, что подводил итоги года с помощью нашего бота! 🤖\n'
             'Хочешь попробовать еще раз и создать новую историю?\n'
             '<code>Воспоминания</code> – это всегда интересно!</b>',
        reply_markup=await end_story_kb()
    )
    await state.clear()
    questions = await get_random_questions(session_maker)
    await state.update_data(questions=questions)


def register_handler(dp: Dispatcher):
    dp.callback_query.register(start_generate, F.data.startswith('choose_style'))
