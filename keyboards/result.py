from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

get_result_keyboard = InlineKeyboardButton(
    text="Отримати результат", callback_data="Result-get"
)
abort_keyboard = InlineKeyboardButton(text="Скасувати", callback_data="Abort-account")


def keyboard_result_lineup_builder(state: str | None = None):
    inline_keyboar_builder = InlineKeyboardBuilder()
    match state:
        case "choose_kb":
            inline_keyboar_builder.add(get_result_keyboard, abort_keyboard)
        case "get_result":
            inline_keyboar_builder.add(abort_keyboard)
    inline_keyboar_builder.adjust(2)
    return inline_keyboar_builder.as_markup()
