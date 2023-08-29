from aiogram import Bot
from aiogram.types import (
    BotCommand,
    BotCommandScopeAllPrivateChats,
)


async def set_menu(bot: Bot):
    commands = [
        BotCommand(
            command="start",
            description="Почати діалог",
        ),
        BotCommand(command="account", description="Зміна полів акаунту"),
        BotCommand(command="group", description="Групи"),
        BotCommand(command="subjectteach", description="Предмети для вчителя"),
        BotCommand(command="subject_s", description="Предмети для учня"),
        BotCommand(command="result", description="Результат"),
        BotCommand(command="logout", description="Вийти з акаунту"),
    ]

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
