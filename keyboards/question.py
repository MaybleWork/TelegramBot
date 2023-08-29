from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

abort_keyboard = InlineKeyboardButton(text="Скасувати", callback_data="Abort-account")

skip_keyboard = InlineKeyboardButton(text="Пропустити", callback_data="Skip")

end_keyboard = InlineKeyboardButton(text="Заверишити", callback_data="End-question")


def keyboard_question_lineup_builder(state: str | None = None):
    inline_keyboar_builder = InlineKeyboardBuilder()
    match state:
        case "enter_text":
            inline_keyboar_builder.add(abort_keyboard, end_keyboard)
        case "enter_max_mark":
            inline_keyboar_builder.add(abort_keyboard)
        case "enter_image" | "enter_file":
            inline_keyboar_builder.add(abort_keyboard, skip_keyboard)
    inline_keyboar_builder.adjust(2)
    return inline_keyboar_builder.as_markup()
