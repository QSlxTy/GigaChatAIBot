from aiogram import types, F, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from sqlalchemy.orm import sessionmaker

from bot_start import bot
from integrations.database.models.user_answers import create_answer_db
from src.config import BotConfig
from utils.states.user import FSMQuestions


async def questions_start(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(
        text='Начнём, вот первый вопрос'
    )
    await state.update_data(answers_list=[])
    await ask_question(call.from_user.id, 0, state)


async def ask_question(chat_id: int, question_index: int, state):
    data = await state.get_data()
    if question_index < len(data['questions']):
        await bot.send_message(
            chat_id=chat_id,
            text=f'{data["questions"][question_index].text}'
        )
        await state.set_state(FSMQuestions.wait_answer)
        await state.update_data(question_index=question_index,
                                chat_id=chat_id)
    else:
        await bot.send_photo(
            chat_id=chat_id,
            photo=FSInputFile(BotConfig.get_photo_path),
            caption='Теперь ты можешь загрузить до четырех своих фотографий,\n'
                    'чтобы сделать комикс еще более персонализированным.\n'
                    'Загрузи одно или несколько фото, которые мне помогут создать образы для твоей истории'
        )
        await state.set_state(FSMQuestions.wait_photo)


async def process_answer(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    data = await state.get_data()
    question_index = data['question_index']
    data['answers_list'].append({'question': data['questions'][question_index].text, 'answer': message.text})
    await create_answer_db(message.from_user.id, data['questions'][question_index].group, message.text, session_maker)
    await ask_question(message.from_user.id, question_index + 1, state)
    await state.update_data(answers_list=data['answers_list'])


def register_handler(dp: Dispatcher):
    dp.callback_query.register(questions_start, F.data == 'go_questions')
    dp.message.register(process_answer, F.content_type == 'text', FSMQuestions.wait_answer)
