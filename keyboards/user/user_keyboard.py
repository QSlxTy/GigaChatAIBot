from aiogram.utils.keyboard import InlineKeyboardBuilder

from integrations.database.models.generation_style import get_all_style_db


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


async def skip_photo_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='Пропустить фото?', callback_data='skip_photo')
    return builder.as_markup()


async def choose_style_kb(session_maker):
    styles = await get_all_style_db(session_maker)
    builder = InlineKeyboardBuilder()
    for style in styles:
        builder.button(text=style.style, callback_data=f'choose_style:{style.text}:{style.style}')
    builder.adjust(1)
    return builder.as_markup()


async def end_story_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='Создать новую историю', callback_data='go_questions')
    return builder.as_markup()
