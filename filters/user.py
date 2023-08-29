from aiogram.filters import BaseFilter
from aiogram.types import Message
from settings.config import bot_db
from validate_email import validate_email


class NoAuthorizedUserFilter(BaseFilter):
    no_auth_user: bool = True

    async def __call__(self, obj: Message) -> bool:
        return (bot_db.exist_user(user_id=obj.from_user.id)) != self.no_auth_user


class AuthorizedUserFilter(BaseFilter):
    user_authorized: bool = True

    async def __call__(self, obj: Message) -> bool:
        return (
            bot_db.exist_user(user_id=obj.from_user.id)
        ) == self.user_authorized  # user_active user_exists


class AuthorizedTeacherFilter(BaseFilter):
    auth_user: bool = True

    async def __call__(self, obj: Message) -> bool:
        return (
            bot_db.exist_user_teacher(user_id=obj.from_user.id)
        ) == self.auth_user  # user_active user_exists


class AuthorizedStudentFilter(BaseFilter):
    auth_user: bool = True

    async def __call__(self, obj: Message) -> bool:
        return (
            bot_db.exist_user_student(user_id=obj.from_user.id)
        ) == self.auth_user  # user_active user_exists


class EmailFilter(BaseFilter):
    valid_email = True

    async def __call__(self, obj: Message) -> bool:
        return validate_email(obj.text.strip()) == self.valid_email
