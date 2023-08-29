from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command


import regex
from typing import Dict, Union


from filters.user import (
    EmailFilter,
    NoAuthorizedUserFilter,
    AuthorizedTeacherFilter,
    AuthorizedStudentFilter,
)
from states.account_states import AccountUpdateStates
from settings.config import bot_db
from samples import templates
from samples.utils import edit_message_text_safe
from keyboards.account import keyboard_account_lineup_builder
from samples.requests import updating_user


unauthorized_user_router = Router()
unauthorized_user_router.message.filter(NoAuthorizedUserFilter())
teacher_user_router = Router()
teacher_user_router.message.filter(AuthorizedTeacherFilter())
student_user_router = Router()
student_user_router.message.filter(AuthorizedStudentFilter())

flags = {"throttling_key": "default"}


@unauthorized_user_router.message(
    Command("account"),
    flags=flags,
)
async def user_account(
    message: Message,
):
    await message.answer(
        text=templates.UNAUTHORIZED_USER_ACCOUNT_MESSAGE,
    )


@teacher_user_router.message(
    Command("account"),
    flags=flags,
)
async def user_account(message: Message, state: FSMContext) -> None:
    answer_msg = await message.answer(
        text=templates.AUTHORIZED_USER_ACCOUNT_MESSAGE,
        reply_markup=keyboard_account_lineup_builder("choose_kb"),
    )
    await state.update_data(edit_message_id=answer_msg.message_id)
    await state.set_state(AccountUpdateStates.choose_kb)


@teacher_user_router.callback_query(
    AccountUpdateStates.choose_kb,
    Text(text=["Account"]),
    flags=flags,
)
async def email_editing_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await call.answer()
    await edit_message_text_safe(
        bot=bot,
        text=templates.START_UPDATING_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_account_lineup_builder(state="update_email"),
    )
    await state.set_state(AccountUpdateStates.update_email)


# -------------------update email-----------------


@teacher_user_router.message(
    AccountUpdateStates.update_email,
    (F.text.len() <= 100) & (F.text.len() >= 0),
    EmailFilter(),
    flags=flags,
)
async def email_updating(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await state.update_data(email_upd=message.text.strip())
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.EMAIL_UPDATING_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_account_lineup_builder(state="update_name"),
    )
    await state.set_state(AccountUpdateStates.update_name)


@teacher_user_router.message(
    AccountUpdateStates.update_email,
    flags=flags,
)
async def email_updating_failed(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.EMAIL_REGISTRATION_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_account_lineup_builder(state="update_email"),
    )


# -------------------update name-----------------


@teacher_user_router.message(
    AccountUpdateStates.update_name,
    (F.text.len() <= 60)
    & (F.text.len() >= 0)
    & (F.text.regexp(regex.compile(r"^[a-zA-Z]+$"))),
    flags=flags,
)
async def name_updating(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await state.update_data(name_upd=message.text.strip())
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.NAME_UPDATING_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_account_lineup_builder(state="update_last_name"),
    )
    await state.set_state(AccountUpdateStates.update_last_name)


@teacher_user_router.message(
    AccountUpdateStates.update_name,
    flags=flags,
)
async def name_updating_failed(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.NAME_REGISTRATION_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_account_lineup_builder(state="update_name"),
    )


# -------------------update last_name-----------------


@teacher_user_router.message(
    AccountUpdateStates.update_last_name,
    (F.text.len() <= 60)
    & (F.text.len() >= 0)
    & (F.text.regexp(regex.compile(r"^[a-zA-Z]+$"))),
    flags=flags,
)
async def last_name_updating(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await state.update_data(last_name_upd=message.text.strip())
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.LAST_NAME_UPDATING_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_account_lineup_builder(state="update_surname"),
    )
    await state.set_state(AccountUpdateStates.update_surname)


@teacher_user_router.message(
    AccountUpdateStates.update_last_name,
    flags=flags,
)
async def last_name_updating_failed(
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
        reply_markup=keyboard_account_lineup_builder(state="update_last_name"),
    )


# -------------------update surname-----------------


@teacher_user_router.message(
    AccountUpdateStates.update_surname,
    (F.text.len() <= 60)
    & (F.text.len() >= 0)
    & (F.text.regexp(regex.compile(r"^[a-zA-Z]+$"))),
    flags=flags,
)
async def surname_updating(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(surname_upd=message.text.strip())
    state_data = await state.get_data()
    await message.delete()

    def check_login_result_error(
        result: Union[None, str, Dict], key: str = "detail"
    ) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = result.get(key, errors)
        return errors

    current_user_email = bot_db.get_email_user(user_id=message.from_user.id)

    status_code, response = await updating_user(
        upd_data={
            "email": state_data.get("email_upd"),
            "name": state_data.get("name_upd"),
            "last_name": state_data.get("last_name_upd"),
            "surname": state_data.get("surname_upd"),
        },
        email=current_user_email,
    )

    await edit_message_text_safe(
        bot=bot,
        text=templates.SURNAME_UPDATING_MESSAGE
        if status_code == 200
        else templates.ERROR_MESSAGE.format(errors=check_login_result_error(response)),
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_account_lineup_builder(),
    )
    if status_code == 200:
        bot_db.update_user_info(
            email=response["email"],
            name=response["name"],
            last_name=response["last_name"],
            surname=response["surname"],
            user_id=message.from_user.id,
        )

    await state.clear()


@teacher_user_router.message(
    AccountUpdateStates.update_surname,
    flags=flags,
)
async def surname_updating_failed(
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
        reply_markup=keyboard_account_lineup_builder(state="update_surname"),
    )
