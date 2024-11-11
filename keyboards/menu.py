from aiogram.utils.keyboard import InlineKeyboardBuilder


async def main_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='...', callback_data='__')
    builder.button(text='...', callback_data='__')
    return builder.as_markup()