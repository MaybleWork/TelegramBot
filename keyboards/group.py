from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

create_group_keyboard = InlineKeyboardButton(
    text="Створити нову групу", callback_data="Group-creation"
)
# update_group_keyboard = InlineKeyboardButton(
#     text="Оновити", callback_data="Group-update"
# )
add_student_group_keyboard = InlineKeyboardButton(
    text="Додати студентів", callback_data="Student-add"
)
abort_keyboard = InlineKeyboardButton(text="Скасувати", callback_data="Abort-account")
end_keyboard = InlineKeyboardButton(text="Завершити", callback_data="End-account")


def keyboard_group_lineup_builder(state: str | None = None):
    inline_keyboar_builder = InlineKeyboardBuilder()
    match state:
        case "choose_keyboard":
            inline_keyboar_builder.add(
                create_group_keyboard,
                add_student_group_keyboard,
                abort_keyboard,
            )
        case "enter_name" | "update_name":
            inline_keyboar_builder.add(abort_keyboard)
        case "add_student":
            inline_keyboar_builder.add(end_keyboard, abort_keyboard)
    inline_keyboar_builder.adjust(2)
    return inline_keyboar_builder.as_markup()
