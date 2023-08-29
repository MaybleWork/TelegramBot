from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def keyboard_logout_lineup_builder():
    logout_builder = InlineKeyboardBuilder()
    logout_builder.add(
        InlineKeyboardButton(text="Вихід", callback_data="logout-true"),
        InlineKeyboardButton(text="Відміна", callback_data="logout-cancel"),
    )

    return logout_builder.as_markup()
