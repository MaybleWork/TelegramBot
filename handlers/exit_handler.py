from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters import Text

from settings.config import bot_db
from filters.user import NoAuthorizedUserFilter, AuthorizedUserFilter
from states.exit_states import LogoutStates
from keyboards.exit import keyboard_logout_lineup_builder
from samples import templates
from samples.utils import edit_message_text_safe

# from samples.requests import auth_logout

unauthorized_user_router = Router()
unauthorized_user_router.message.filter(NoAuthorizedUserFilter())
authorized_user_router = Router()
authorized_user_router.message.filter(AuthorizedUserFilter())

flags = {"throttling_key": "default"}


@unauthorized_user_router.message(
    Command("logout"),
    flags=flags,
)
async def user_logout(message: Message):
    await message.answer(
        text=templates.UNAUTHORIZED_USER_ACCOUNT_MESSAGE,
        parse_mode=None,
    )


@authorized_user_router.message(
    Command("logout"),
    flags=flags,
)
async def user_logout(message: Message, state: FSMContext):
    answer_msg = await message.answer(
        text=templates.LOGOUT_USER_MESSAGE,
        parse_mode=None,
        reply_markup=keyboard_logout_lineup_builder(),
    )
    await state.update_data(edited_msg_id=answer_msg.message_id)
    await state.set_state(LogoutStates.logout)


@authorized_user_router.callback_query(LogoutStates.logout, Text("logout-true"))
async def callbacks_logout(call: CallbackQuery, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    bot_db.delete_user(call.from_user.id)
    await edit_message_text_safe(
        bot=bot,
        text="Ви вийшли з акаунту, щоб працювати з ботом, пройдіть авторизацію",
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edited_msg_id"],
        reply_markup=None,
    )
    await call.answer()
    await state.clear()


@authorized_user_router.callback_query(LogoutStates.logout, Text("logout-cancel"))
async def callbacks_logout(call: CallbackQuery, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    await edit_message_text_safe(
        bot=bot,
        text=templates.LOGOUT_USER_CANCEL_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edited_msg_id"],
        reply_markup=None,
    )
    await call.answer()
