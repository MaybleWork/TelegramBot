from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

account_keyboard = InlineKeyboardButton(
    text="Змінити поля акаунту", callback_data="Account"
)
abort_keyboard = InlineKeyboardButton(text="Скасувати", callback_data="Abort-account")


def keyboard_account_lineup_builder(state: str | None = None):
    inline_keyboar_builder = InlineKeyboardBuilder()
    match state:
        case "choose_kb":
            inline_keyboar_builder.add(account_keyboard, abort_keyboard)
        case "update_email" | "update_name" | "update_last_name" | "update_surname":
            inline_keyboar_builder.add(abort_keyboard)
    inline_keyboar_builder.adjust(2)
    return inline_keyboar_builder.as_markup()
