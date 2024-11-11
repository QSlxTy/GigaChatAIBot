from aiogram.utils.keyboard import InlineKeyboardBuilder


async def back_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='🔙 В главное меню', callback_data='main_menu')
    return builder.as_markup()


async def start_agree_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='Да', callback_data='start_agree')
    return builder.as_markup()


async def agree_rules_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='Я согласен', callback_data='agree_rules')
    return builder.as_markup()


async def go_questions_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='Далее', callback_data='go_questions')
    return builder.as_markup()
