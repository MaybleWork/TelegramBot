from aiogram import Router, F
from aiogram.types import Message, ContentType
from aiogram.filters.command import (
    CommandObject,
    CommandStart,
    Command,
)

from samples.templates import *
from keyboards.registration import keyboard_auth_lineup_builder
from filters.user import NoAuthorizedUserFilter, AuthorizedUserFilter
from settings.config import bot_db
from samples import templates


unauthorized_user_router = Router()
unauthorized_user_router.message.filter(NoAuthorizedUserFilter())
authorized_user_router = Router()
authorized_user_router.message.filter(AuthorizedUserFilter())

flags = {"throttling_key": "default"}


@unauthorized_user_router.message(
    CommandStart(),
    flags=flags,
)
async def user_start(
    message: Message,
):
    await message.answer(
        text=templates.UNAUTHORIZED_USER_START_MESSAGE,
        reply_markup=keyboard_auth_lineup_builder(),
    )


@authorized_user_router.message(
    CommandStart(),
    flags=flags,
)
async def user_start(message: Message):
    await message.answer(
        templates.AUTHORIZED_USER_START_MESSAGE.format(
            user=bot_db.get_full_name_user(message.from_user.id)
        )
    )
