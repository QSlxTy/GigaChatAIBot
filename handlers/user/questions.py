from aiogram import types, F, Dispatcher
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from bot_start import bot
from integrations.database.models.user_answers import create_answer_db
from utils.states.user import FSMQuestions


async def questions_start(call: types.CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    data = await state.get_data()
    try:
        msg = await data['msg'].edit_text(
            text="<b>Начнём, вот первый вопрос</b>")
    except (KeyError, TelegramBadRequest):
        await call.message.delete()
        msg = await call.message.answer(
            text="<b>Начнём, вот первый вопрос</b>")
    await state.update_data(msg=msg, answers_list=[])
    await ask_question(call.from_user.id, 0, state, msg.message_id)


async def ask_question(chat_id: int, question_index: int, state, msg_id):
    data = await state.get_data()
    if question_index < len(data['questions']):
        await bot.edit_message_text(chat_id=chat_id,
                                    message_id=msg_id,
                                    text=data['questions'][question_index].text)
        await state.set_state(FSMQuestions.wait_answer)
        await state.update_data(question_index=question_index,
                                chat_id=chat_id,
                                message_id=msg_id, )
    else:
        msg = await bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text="<b>Теперь ты можешь загрузить до четырех своих фотографий, "
                 "чтобы сделать комикс еще более персонализированным. "
                 "Загрузи одно или несколько фото, которые мне помогут создать образы для твоей истории</b>")
        await state.set_state(FSMQuestions.wait_photo)
        await state.update_data(msg=msg)


async def process_answer(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    data = await state.get_data()
    await message.delete()
    question_index = data['question_index']
    data['answers_list'].append({'question': data['questions'][question_index].text, 'answer': message.text})
    await create_answer_db(message.from_user.id, data['questions'][question_index].group, message.text,session_maker)
    await ask_question(message.from_user.id, question_index + 1, state, data['message_id'])
    await state.update_data(answers_list=data['answers_list'])


def register_handler(dp: Dispatcher):
    dp.callback_query.register(questions_start, F.data == 'go_questions')
    dp.message.register(process_answer, F.content_type == 'text', FSMQuestions.wait_answer)
