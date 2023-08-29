from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


create_group_keyboard = InlineKeyboardButton(
    text="Створити новий предмет", callback_data="Subject-creation"
)
update_group_keyboard = InlineKeyboardButton(
    text="Отримати", callback_data="Subject-update"
)
add_keyboard = InlineKeyboardButton(text="Додати питання", callback_data="Add-question")
add_test_keyboard = InlineKeyboardButton(text="Додати тест", callback_data="Add-test")
abort_keyboard = InlineKeyboardButton(text="Скасувати", callback_data="Abort-account")
update_keyboard = InlineKeyboardButton(text="Оновити", callback_data="Update-test")
result_keyboard = InlineKeyboardButton(
    text="Переглянути результати", callback_data="Result-get"
)
end_keyboard = InlineKeyboardButton(text="Завершити", callback_data="End-account")


def keyboard_subject_teacher_lineup_builder(state: str | None = None):
    inline_keyboar_builder = InlineKeyboardBuilder()
    match state:
        case "choose_keyboard":
            inline_keyboar_builder.add(
                create_group_keyboard,
                update_group_keyboard,
                add_test_keyboard,
                abort_keyboard,
            )
        case "result":
            inline_keyboar_builder.add(
                result_keyboard, add_keyboard, update_keyboard, abort_keyboard
            )
        case "answer":
            inline_keyboar_builder.add(end_keyboard, abort_keyboard)
        case "enter_title" | "enter_group":
            inline_keyboar_builder.add(abort_keyboard)
    inline_keyboar_builder.adjust(2)
    return inline_keyboar_builder.as_markup()
