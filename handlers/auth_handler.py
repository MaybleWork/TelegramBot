from aiogram import Router, Bot, F
from filters.user import EmailFilter, NoAuthorizedUserFilter, AuthorizedUserFilter
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from typing import Dict, Union
from settings.config import bot_db

from states.auth_states import UserRegistrationStates
from samples.utils import edit_message_text_safe
from samples.requests import authorization_user
from samples import templates
from keyboards.registration import keyboard_auth_lineup_builder


unauthorized_user_router = Router()
unauthorized_user_router.message.filter(NoAuthorizedUserFilter())
authorized_user_router = Router()
authorized_user_router.message.filter(AuthorizedUserFilter())

flags = {"throttling_key": "default"}


@unauthorized_user_router.callback_query(
    StateFilter(
        *[
            UserRegistrationStates.choose_keyboard,
            UserRegistrationStates.reg_teacher.start_auth,
            UserRegistrationStates.reg_student.start_auth,
        ]
    ),
    Text(text=["Authorization"]),
    flags=flags,
)
async def authorization_email_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await edit_message_text_safe(
        bot=bot,
        text=templates.AUTHORIZTION_USER_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_auth_lineup_builder("enter_email_login"),
    )

    await state.set_state(UserRegistrationStates.auth.enter_email_login)


# ------ authorization, email enterance


@unauthorized_user_router.message(
    UserRegistrationStates.auth.enter_email_login,
    (F.text.len() <= 100) & (F.text.len() >= 1),
    EmailFilter(),
    flags=flags,
)
async def auhtorization_email_entering(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await state.update_data(user_authorization_email=message.text.strip())
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.AUTHORIZATION_USER_PASS_ENTERING,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_auth_lineup_builder(state="enter_password"),
    )
    await state.set_state(UserRegistrationStates.auth.enter_password)


@unauthorized_user_router.message(
    UserRegistrationStates.auth.enter_email_login,
    flags=flags,
)
async def auth_email_entered_incorrectly(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.EMAIL_AUNTHORIZATION_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_auth_lineup_builder(state="enter_email_login"),
    )


# ------ authorization, password enterance


@unauthorized_user_router.message(
    UserRegistrationStates.auth.enter_password,
    (F.text.len() <= 100) & (F.text.len() >= 7),
    flags=flags,
)
async def password_entered(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(user_authorization_password=message.text.strip())
    await message.delete()
    state_data = await state.get_data()

    def check_login_result_error(
        result: Union[None, str, Dict], key: str = "detail"
    ) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = result.get(key, errors)
        return errors

    status_code, response = await authorization_user(
        auth_data={
            "email": state_data.get("user_authorization_email"),
            "password": state_data.get("user_authorization_password"),
        }
    )
    await edit_message_text_safe(
        bot=bot,
        text=templates.AUTHORIZATION_PASSWORD_MESSAGE
        if status_code == 200
        else templates.ERROR_MESSAGE.format(errors=check_login_result_error(response)),
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_auth_lineup_builder(),
    )
    if status_code == 200:
        bot_db.add_user(
            user_id=message.from_user.id,
            name=response["user"]["name"],
            last_name=response["user"]["last_name"],
            surname=response["user"]["surname"],
            email=response["user"]["email"],
            token=response["token"],
            user_type=response["user"]["user_type"],
        )
    await state.clear()


@unauthorized_user_router.message(
    UserRegistrationStates.auth.enter_password,
    flags=flags,
)
async def password_entered_incorrectly(
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
