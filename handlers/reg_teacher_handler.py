from aiogram import Router, Bot, F
from filters.user import (
    EmailFilter,
    NoAuthorizedUserFilter,
    AuthorizedTeacherFilter,
    AuthorizedStudentFilter,
)
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

import regex
from typing import Any, Dict, Optional, Union

from states.auth_states import UserRegistrationStates
from samples.utils import edit_message_text_safe, get_errors_from_dict
from samples.requests import teacher_reg_request, verif_code_request
from samples import templates
from keyboards.registration import keyboard_auth_lineup_builder


unauthorized_user_router = Router()
unauthorized_user_router.message.filter(NoAuthorizedUserFilter())
teacher_user_router = Router()
teacher_user_router.message.filter(AuthorizedTeacherFilter())
student_user_router = Router()
student_user_router.message.filter(AuthorizedStudentFilter())

flags = {"throttling_key": "default"}


@unauthorized_user_router.callback_query(
    UserRegistrationStates.choose_keyboard,
    Text(text=["Teacher-registration"]),
    flags=flags,
)
async def email_registration_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await call.answer()
    await edit_message_text_safe(
        bot=bot,
        text=templates.START_REGISTRATION_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_auth_lineup_builder(state="enter_email"),
    )
    await state.set_state(UserRegistrationStates.reg_teacher.enter_email_login)


# -------------------enter email address-----------------


@unauthorized_user_router.message(
    UserRegistrationStates.reg_teacher.enter_email_login,
    (F.text.len() <= 100) & (F.text.len() >= 1),
    EmailFilter(),
    flags=flags,
)
async def email_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await state.update_data(email=message.text.strip())
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.EMAIL_REGISTRATION_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_auth_lineup_builder(state="enter_name"),
    )
    await state.set_state(UserRegistrationStates.reg_teacher.enter_name)


@unauthorized_user_router.message(
    UserRegistrationStates.reg_teacher.enter_email_login,
    flags=flags,
)
async def email_entering_failed(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.EMAIL_REGISTRATION_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_auth_lineup_builder(state="enter_email"),
    )


# -------------------enter name-----------------


@unauthorized_user_router.message(
    UserRegistrationStates.reg_teacher.enter_name,
    (F.text.len() <= 60)
    & (F.text.len() >= 1)
    & (F.text.regexp(regex.compile(r"^[a-zA-Z]+$"))),
    flags=flags,
)
async def name_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await state.update_data(name=message.text.strip())
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.NAME_REGISTRATION_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_auth_lineup_builder(state="enter_last_name"),
    )
    await state.set_state(UserRegistrationStates.reg_teacher.enter_last_name)


@unauthorized_user_router.message(
    UserRegistrationStates.reg_teacher.enter_name,
    flags=flags,
)
async def name_entering_failed(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.NAME_REGISTRATION_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_auth_lineup_builder(state="enter_name"),
    )


# -------------------enter last name-----------------


@unauthorized_user_router.message(
    UserRegistrationStates.reg_teacher.enter_last_name,
    (F.text.len() <= 60)
    & (F.text.len() >= 1)
    & (F.text.regexp(regex.compile(r"^[a-zA-Z]+$"))),
    flags=flags,
)
async def last_name_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await state.update_data(last_name=message.text.strip())
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.LAST_NAME_REGISTRATION_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_auth_lineup_builder(state="enter_surname"),
    )
    await state.set_state(UserRegistrationStates.reg_teacher.enter_surname)


@unauthorized_user_router.message(
    UserRegistrationStates.reg_teacher.enter_name,
    flags=flags,
)
async def last_name_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.LAST_NAME_REGISTRATION_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_auth_lineup_builder(state="enter_last_name"),
    )


# -------------------enter surname-----------------


@unauthorized_user_router.message(
    UserRegistrationStates.reg_teacher.enter_surname,
    (F.text.len() <= 60)
    & (F.text.len() >= 1)
    & (F.text.regexp(regex.compile(r"^[a-zA-Z]+$"))),
    flags=flags,
)
async def surname_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await state.update_data(surname=message.text.strip())
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.SURNAME_REGISTRATION_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_auth_lineup_builder(state="enter_password"),
    )
    await state.set_state(UserRegistrationStates.reg_teacher.enter_password)


@unauthorized_user_router.message(
    UserRegistrationStates.reg_teacher.enter_surname,
    flags=flags,
)
async def surname_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.SURNAME_REGISTRATION_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_auth_lineup_builder(state="enter_surname"),
    )


# -------------------enter password-----------------


@unauthorized_user_router.message(
    UserRegistrationStates.reg_teacher.enter_password,
    (F.text.len() <= 100)
    & (F.text.len() >= 10)
    & (F.text.regexp(regex.compile(r"^(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=*]).+$"))),
    flags=flags,
)
async def password_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await state.update_data(password=message.text.strip())
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.PASSWORD_TEACHER_REGISTRATION_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_auth_lineup_builder(state="enter_verif_code"),
    )
    await state.set_state(UserRegistrationStates.reg_teacher.enter_verif_code)


@unauthorized_user_router.message(
    UserRegistrationStates.reg_teacher.enter_password,
    flags=flags,
)
async def password_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.PASSWORD_REGISTRATION_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_auth_lineup_builder(state="enter_password"),
    )


# -------------------enter verification code-----------------


@unauthorized_user_router.message(
    UserRegistrationStates.reg_teacher.enter_verif_code,
    flags=flags,
)
async def verif_code_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(verif_code=message.text.strip())
    state_data = await state.get_data()
    await message.delete()

    def register_result_error(
        reg_result: Union[None, str, Dict], verif_result: Union[None, str, Dict]
    ) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if (
            reg_result
            and reg_result != "Timeout"
            and verif_result
            and verif_result != "Timeout"
        ):
            errors = get_errors_from_dict(errors_dict=reg_result)
        return errors

    verif_result = await verif_code_request(
        verification_code=state_data.get("verif_code")
    )

    reg_result = await teacher_reg_request(
        collected_data={
            "email": state_data.get("email"),
            "password": state_data.get("password"),
            "name": state_data.get("name"),
            "last_name": state_data.get("last_name"),
            "surname": state_data.get("surname"),
        }
    )

    errors_text = register_result_error(reg_result, verif_result)

    await edit_message_text_safe(
        bot=bot,
        text=templates.VERIF_CODE_REGISTRATION_MESSAGE
        if not verif_result and not reg_result
        else templates.ERROR_MESSAGE.format(errors=errors_text),
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_auth_lineup_builder(),
    )

    if not verif_result and not reg_result:
        await state.set_state(UserRegistrationStates.reg_teacher.start_auth)
    else:
        await state.clear()


@unauthorized_user_router.message(
    UserRegistrationStates.reg_teacher.enter_verif_code,
    flags=flags,
)
async def verif_code_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.VERIF_CODE_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_auth_lineup_builder(state="enter_verif_code"),
    )
