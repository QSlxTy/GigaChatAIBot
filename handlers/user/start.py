import time

from aiogram import types, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from sqlalchemy.orm import sessionmaker

from integrations.database.models.questions import get_random_questions
from integrations.database.models.user import update_user_db, get_user_db
from keyboards.user.user_keyboard import agree_rules_kb, go_questions_kb
from src.config import BotConfig
from utils.states.user import FSMStart


async def start_command(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    await state.set_state(FSMStart.start)
    user_info = await get_user_db({'telegram_id': message.from_user.id}, session_maker)
    if user_info.agreed is True:
        await message.answer_photo(
            photo=FSInputFile(BotConfig.start_photo_path),
            caption='Для создания истории я задам вам несколько вопросов. Отвечайте честно и по '
                    'возможности подробно — это поможет создать по-настоящему уникальную историю!',
            reply_markup=await go_questions_kb()
        )
        questions = await get_random_questions(session_maker)
        await state.update_data(questions=questions)
    else:
        await message.answer(
            text='Правила пользования ботом:\n\n'
                 'Начиная использование Telegram-бота, вы соглашаетесь с <a href="https://sbercity.ru/media/ss/sd/f/%D0%9F%D0%BE%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%D0%B0_%D0%BE%D0%B1%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B8_%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85_%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85.pdf">Политикой конфиденциальности</a>\n'
                 'Обращаем внимание, что текстовые запросы, а также графические объекты, которые вы создаёте в этом боте (далее по тексту — «Пользовательский контент»), не должны нарушать законодательство Российской Федерации и общепризнанные этические правила и нормы.\n'
                 'Вся ответственность за Пользовательский контент лежит на пользователе.\n'
                 'В случае вопросов, пожалуйста, обращайтесь по почте: <code>ASidelnikov@sbercity.ru</code>',
            reply_markup=await agree_rules_kb()
        )


async def agree_rules(call: types.CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    await update_user_db(call.from_user.id, {'agreed': True}, session_maker)
    user_info = await get_user_db({'telegram_id': call.from_user.id}, session_maker)
    if user_info.agreed is True:
        await call.message.answer(
            text='Отлично!'
        )
        time.sleep(2)
        await call.message.answer_photo(
            photo=FSInputFile(BotConfig.start_photo_path),
            caption='Для создания истории я задам вам несколько вопросов. Отвечайте честно и по '
                    'возможности подробно — это поможет создать по-настоящему уникальную историю!',
            reply_markup=await go_questions_kb()
        )
        questions = await get_random_questions(session_maker)
        await state.update_data(questions=questions)
    else:
        await call.message.answer(
            text='Правила пользования ботом:\n\n'
                 'Начиная использование Telegram-бота, вы соглашаетесь с <a href="https://sbercity.ru/media/ss/sd/f/%D0%9F%D0%BE%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%D0%B0_%D0%BE%D0%B1%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B8_%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85_%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85.pdf">Политикой конфиденциальности</a>\n'
                 'Обращаем внимание, что текстовые запросы, а также графические объекты, которые вы создаёте в этом боте (далее по тексту — «Пользовательский контент»), не должны нарушать законодательство Российской Федерации и общепризнанные этические правила и нормы.\n'
                 'Вся ответственность за Пользовательский контент лежит на пользователе.\n'
                 'В случае вопросов, пожалуйста, обращайтесь по почте: <code>ASidelnikov@sbercity.ru</code>',
            reply_markup=await agree_rules_kb()
        )


def register_start_handler(dp: Dispatcher):
    dp.message.register(start_command, Command('start'))
    dp.callback_query.register(agree_rules, F.data == 'agree_rules')
