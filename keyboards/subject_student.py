from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


get_group_keyboard = InlineKeyboardButton(text="Отримати", callback_data="Group-get")

abort_keyboard = InlineKeyboardButton(text="Скасувати", callback_data="Abort-account")

previous_keyboard = InlineKeyboardButton(text="Попереднє", callback_data=f"Previous")

next_keyboard = InlineKeyboardButton(text="Наступне", callback_data=f"Next")

test_end_keyboard = InlineKeyboardButton(
    text="Завершити тест", callback_data=f"Test-end"
)


def keyboard_subject_student_lineup_builder(
    state: str | None = None,
    question_data: str | None = None,
    backstep: bool | None = None,
):
    inline_keyboar_builder = InlineKeyboardBuilder()
    match state:
        case "choose_keyboard":
            inline_keyboar_builder.add(get_group_keyboard, abort_keyboard)
        case "enter_test_title":
            inline_keyboar_builder.add(abort_keyboard)
        case "send_answer":
            if backstep == True and question_data["previous"] and question_data["next"]:
                inline_keyboar_builder.add(
                    previous_keyboard,
                    next_keyboard,
                    test_end_keyboard,
                )
            elif (
                backstep == False
                and question_data["previous"]
                and question_data["next"]
            ):
                inline_keyboar_builder.add(next_keyboard, test_end_keyboard)
            elif not question_data["previous"] and question_data["next"]:
                inline_keyboar_builder.add(next_keyboard, test_end_keyboard)
            else:
                inline_keyboar_builder.add(previous_keyboard, test_end_keyboard)
    inline_keyboar_builder.adjust(2)
    return inline_keyboar_builder.as_markup()
