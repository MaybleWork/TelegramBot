from aiogram import Bot, Dispatcher
from aiogram import Bot, Dispatcher


from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

from samples.menu import set_menu
from settings.config import config
from handlers import (
    auth_handler,
    default_handler,
    reg_student_handler,
    reg_teacher_handler,
    account_handler,
    group_handler,
    subject_handler,
    test_handler,
    question_handler,
    answer_handler,
    result_handler,
    exit_handler,
)
from middlewares.throttling import ThrottlingMiddleware


def _register_global_middlewares(dp: Dispatcher, bot: Bot):
    dp.message.middleware(ThrottlingMiddleware(bot))


async def main():
    storage = MemoryStorage()

    bot = Bot(token=config.bot_token.get_secret_value())

    dp = Dispatcher(storage=storage)

    for router in [
        auth_handler.authorized_user_router,
        auth_handler.unauthorized_user_router,
        reg_student_handler.student_user_router,
        reg_student_handler.teacher_user_router,
        reg_student_handler.unauthorized_user_router,
        reg_teacher_handler.teacher_user_router,
        reg_teacher_handler.student_user_router,
        reg_teacher_handler.unauthorized_user_router,
        account_handler.unauthorized_user_router,
        account_handler.student_user_router,
        account_handler.teacher_user_router,
        group_handler.unauthorized_user_router,
        group_handler.student_user_router,
        group_handler.teacher_user_router,
        subject_handler.unauthorized_user_router,
        subject_handler.student_user_router,
        subject_handler.teacher_user_router,
        test_handler.teacher_user_router,
        test_handler.student_user_router,
        question_handler.teacher_user_router,
        answer_handler.teacher_user_router,
        result_handler.unauthorized_user_router,
        result_handler.teacher_user_router,
        result_handler.student_user_router,
        exit_handler.authorized_user_router,
        exit_handler.unauthorized_user_router,
        default_handler.student_user_router,
        default_handler.teacher_user_router,
        default_handler.unauthorized_user_router,
    ]:
        dp.include_router(router)

    _register_global_middlewares(dp, bot)

    await set_menu(bot)

    try:
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
        )
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
