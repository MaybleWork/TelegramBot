from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

abort_keyboard = InlineKeyboardButton(text="Скасувати", callback_data="Abort-account")

end_keyboard = InlineKeyboardButton(text="Заверишити", callback_data="End-question")

add_test_answer_end_keyboard = InlineKeyboardButton(
    text="Тестова відповідь(одна)", callback_data="Test-answer"
)

add_multitest_answer_end_keyboard = InlineKeyboardButton(
    text="Тестова відповідь(декілька)", callback_data="Multitest-answer"
)
add_text_answer_end_keyboard = InlineKeyboardButton(
    text="Відкрита відповідь", callback_data="Text-answer"
)
question_add_keyboard = InlineKeyboardButton(
    text="Додати запитання", callback_data="Question-add"
)
true_keyboard = InlineKeyboardButton(text="Так", callback_data="True")

false_keyboard = InlineKeyboardButton(text="Ні", callback_data="False")


def keyboard_answer_lineup_builder(state: str | None = None):
    inline_keyboar_builder = InlineKeyboardBuilder()
    match state:
        case "add_answer":
            inline_keyboar_builder.add(
                add_test_answer_end_keyboard,
                add_multitest_answer_end_keyboard,
                add_text_answer_end_keyboard,
                abort_keyboard,
                end_keyboard,
            )
        case "test_enterance":
            inline_keyboar_builder.add(question_add_keyboard, abort_keyboard)
        case "mark_enterance":
            inline_keyboar_builder.add(abort_keyboard)
        case "test_start":
            inline_keyboar_builder.add(end_keyboard, abort_keyboard)
        case "true_false":
            inline_keyboar_builder.add(true_keyboard, false_keyboard, abort_keyboard)
    inline_keyboar_builder.adjust(2)
    return inline_keyboar_builder.as_markup()
