from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

abort_keyboard = InlineKeyboardButton(text="Скасувати", callback_data="Abort-account")

true_keyboard = InlineKeyboardButton(text="Так", callback_data="True")

false_keyboard = InlineKeyboardButton(text="Ні", callback_data="False")

end_keyboard = InlineKeyboardButton(text="Завершити", callback_data="End-test")


def keyboard_test_lineup_builder(state: str | None = None):
    inline_keyboar_builder = InlineKeyboardBuilder()
    match state:
        case "enter_test_title":
            inline_keyboar_builder.add(end_keyboard, abort_keyboard)
        case "enter":
            inline_keyboar_builder.add(abort_keyboard)
        case "true_false":
            inline_keyboar_builder.add(true_keyboard, false_keyboard, abort_keyboard)
    inline_keyboar_builder.adjust(2)
    return inline_keyboar_builder.as_markup()
