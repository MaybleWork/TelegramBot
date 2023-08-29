from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest


async def edit_message_text_safe(
    bot: Bot, text, parse_mode, chat_id, message_id, reply_markup
):
    try:
        await bot.edit_message_text(
            text=text,
            parse_mode=parse_mode,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=reply_markup,
        )
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            raise e


def get_errors_from_dict(errors_dict: dict, key_name: str = "errors") -> str:
    error_messages = []

    for field, errors in errors_dict.get(key_name, {}).items():
        for error in errors:
            error_messages.append(f"{field.capitalize()}: {error}")

    return "\n".join(error_messages)
