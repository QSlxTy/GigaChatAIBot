from aiogram.fsm.state import State, StatesGroup


class FSMStart(StatesGroup):
    start = State()


class FSMQuestions(StatesGroup):
    wait_answer = State()
    wait_photo = State()
