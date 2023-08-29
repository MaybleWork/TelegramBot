from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


auth_keyboard = InlineKeyboardButton(text="Авторизація", callback_data="Authorization")
student_reg_keyboard = InlineKeyboardButton(
    text="Реєстрація(Студент)", callback_data="Student-registration"
)
teacher_reg_keyboard = InlineKeyboardButton(
    text="Реєстрація(Вчитель)", callback_data="Teacher-registration"
)
abort_keyboard = InlineKeyboardButton(
    text="Скасувати", callback_data="Abort-authorization"
)


def keyboard_auth_lineup_builder(state: str | None = None):
    inline_keyboar_builder = InlineKeyboardBuilder()
    match state:
        case "choose_keyboard":
            inline_keyboar_builder.add(
                auth_keyboard,
                student_reg_keyboard,
                teacher_reg_keyboard,
                abort_keyboard,
            )
        case "authorization":
            inline_keyboar_builder.add(auth_keyboard, abort_keyboard)
        case "enter_email_login" | "enter_name" | "enter_surname" | "enter_last_name" | "enter_password" | "enter_verif_code":
            inline_keyboar_builder.add(abort_keyboard)

    inline_keyboar_builder.adjust(2)
    return inline_keyboar_builder.as_markup()
