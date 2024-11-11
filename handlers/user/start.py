import time

from aiogram import types, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from integrations.database.models.questions import get_random_questions
from integrations.database.models.user import update_user_db
from keyboards.user.user_keyboard import agree_rules_kb, start_agree_kb, go_questions_kb
from utils.states.user import FSMStart


async def start_command(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.set_state(FSMStart.start)
    await message.delete()
    try:
        msg = await data['msg'].edit_text(
            text="<b>Привет! Я бот, который поможет тебе подвести итоги твоего года с помощью персонализированного "
                 "комикса. Впереди тебя ждет увлекательное путешествие по воспоминаниям! Начнем?</b>",
            reply_markup=await start_agree_kb())
    except (KeyError, TelegramBadRequest):
        msg = await message.answer(
            text="<b>Привет! Я бот, который поможет тебе подвести итоги твоего года с помощью персонализированного "
                 "комикса. Впереди тебя ждет увлекательное путешествие по воспоминаниям! Начнем?</b>",
            reply_markup=await start_agree_kb())
    await state.update_data(msg=msg)


async def agree_rules(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        msg = await data['msg'].edit_text(
            text="<b>Перед началом ознакомься с нашей офертой <code>[ссылка на оферту]</code></b>",
            reply_markup=await agree_rules_kb())
    except (KeyError, TelegramBadRequest):
        await call.message.delete()
        msg = await call.message.answer(
            text="<b>Перед началом ознакомься с нашей офертой <code>[ссылка на оферту]</code></b>",
            reply_markup=await agree_rules_kb())
    await state.update_data(msg=msg)


async def go_questions(call: types.CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    data = await state.get_data()
    await update_user_db(call.from_user.id, {'agreed': True}, session_maker)
    try:
        msg = await data['msg'].edit_text(text='Отлично!')
        #time.sleep(2)
        msg = await msg.edit_text(
            text='<b>Для создания истории я задам тебе несколько вопросов. Ответь честно и по '
                 'возможности подробно — это поможет создать по-настоящему уникальную историю!</b>',
            reply_markup=await go_questions_kb())
    except (KeyError, TelegramBadRequest):
        await call.message.delete()
        msg = await call.message.answer(text='Отлично!')
        #time.sleep(2)
        msg = await msg.edit_text(
            text='<b>Для создания истории я задам тебе несколько вопросов. Ответь честно и по '
                 'возможности подробно — это поможет создать по-настоящему уникальную историю!</b>',
            reply_markup=await go_questions_kb())
    questions = await get_random_questions(session_maker)
    await state.update_data(msg=msg, questions=questions)


async def main_menu(call: types.CallbackQuery, state: FSMContext):
    ...


def register_start_handler(dp: Dispatcher):
    dp.message.register(start_command, Command('start'))
    dp.callback_query.register(main_menu, F.data == 'main_menu')
    dp.callback_query.register(agree_rules, F.data == 'start_agree')
    dp.callback_query.register(go_questions, F.data == 'agree_rules')
