from aiogram import Router, Bot, F
from filters.user import (
    NoAuthorizedUserFilter,
    AuthorizedTeacherFilter,
    AuthorizedStudentFilter,
)
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from aiogram.filters.command import CommandStart

from settings.config import bot_db
from states.auth_states import UserRegistrationStates
from samples.utils import edit_message_text_safe
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
    StateFilter(
        *[
            UserRegistrationStates.choose_keyboard,
            UserRegistrationStates.reg_teacher.enter_email_login,
            UserRegistrationStates.reg_teacher.enter_name,
            UserRegistrationStates.reg_teacher.enter_last_name,
            UserRegistrationStates.reg_teacher.enter_surname,
            UserRegistrationStates.reg_teacher.enter_password,
            UserRegistrationStates.reg_teacher.enter_verif_code,
            UserRegistrationStates.reg_teacher.start_auth,
            UserRegistrationStates.reg_student.enter_email_login,
            UserRegistrationStates.reg_student.enter_name,
            UserRegistrationStates.reg_student.enter_last_name,
            UserRegistrationStates.reg_student.enter_surname,
            UserRegistrationStates.reg_student.enter_password,
            UserRegistrationStates.reg_student.start_auth,
            UserRegistrationStates.auth.enter_email_login,
            UserRegistrationStates.auth.enter_password,
        ]
    ),
    Text(text=["Abort-authorization"]),
    flags=flags,
)
async def abort_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await call.answer(text="Скасування", show_alert=True)
    await edit_message_text_safe(
        bot=bot,
        text=templates.ABORT_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_auth_lineup_builder(),
    )
    await state.clear()


@teacher_user_router.message(
    CommandStart(),
    flags=flags,
)
async def start_command(message: Message) -> None:
    return await message.answer(
        text=templates.AUTHORIZED_USER_MESSAGE.format(
            user=bot_db.get_full_name_user(message.from_user.id)
        ),
        parse_mode=None,
    )


@student_user_router.message(
    CommandStart(),
    flags=flags,
)
async def start_command(message: Message) -> None:
    return await message.answer(
        text=templates.AUTHORIZED_USER_MESSAGE.format(
            user=bot_db.get_full_name_user(message.from_user.id)
        ),
        parse_mode=None,
    )


@unauthorized_user_router.message(
    CommandStart(),
    flags=flags,
)
async def start_command(message: Message, state: FSMContext) -> None:
    answer_msg = await message.answer(
        text=templates.UNAUTHORIZED_USER_MESSAGE,
        parse_mode=None,
        reply_markup=keyboard_auth_lineup_builder("choose_keyboard"),
    )
    await state.update_data(edit_message_id=answer_msg.message_id)
    await state.set_state(UserRegistrationStates.choose_keyboard)


@teacher_user_router.callback_query(
    flags=flags,
)
async def delete_outstanding_callback_operations(call: CallbackQuery, bot: Bot):
    await call.answer(text="outstanding operation", show_alert=True)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


@student_user_router.callback_query(
    flags=flags,
)
async def delete_outstanding_callback_operations(call: CallbackQuery, bot: Bot):
    await call.answer(text="outstanding operation", show_alert=True)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


@unauthorized_user_router.callback_query(
    flags=flags,
)
async def delete_outstanding_callback_operations(call: CallbackQuery, bot: Bot):
    await call.answer(text="outstanding operation", show_alert=True)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


@teacher_user_router.message(
    flags=flags,
)
async def delete_outstanding_messages(message: Message):
    await message.delete()


@student_user_router.message(
    flags=flags,
)
async def delete_outstanding_messages(message: Message):
    await message.delete()


@unauthorized_user_router.message(
    flags=flags,
)
async def delete_outstanding_messages(message: Message):
    await message.delete()
