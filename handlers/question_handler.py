import json
from aiogram import Router, Bot, F
from filters.user import (
    NoAuthorizedUserFilter,
    AuthorizedTeacherFilter,
    AuthorizedStudentFilter,
)
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

# from aiogram.dispatcher.filters import ContentTypeFilter


import regex
from typing import Dict, Union

from states.subject_states import SubjectStates
from samples.utils import edit_message_text_safe, get_errors_from_dict
from samples.requests import question_creation_request
from samples import templates
from keyboards.question import keyboard_question_lineup_builder
from keyboards.answer import keyboard_answer_lineup_builder

unauthorized_user_router = Router()
unauthorized_user_router.message.filter(NoAuthorizedUserFilter())
teacher_user_router = Router()
teacher_user_router.message.filter(AuthorizedTeacherFilter())
student_user_router = Router()
student_user_router.message.filter(AuthorizedStudentFilter())

flags = {"throttling_key": "default"}


# -------------------question end operation-----------------


@teacher_user_router.callback_query(
    SubjectStates.enter_question_text,
    Text(text=["End-question"]),
    flags=flags,
)
async def subject_end_operation_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await call.answer()
    await edit_message_text_safe(
        bot=bot,
        text=templates.GROUP_END_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_question_lineup_builder(),
    )
    await state.clear()


@teacher_user_router.callback_query(
    SubjectStates.choose_keyboard,
    Text(text=["Add-question"]),
    flags=flags,
)
async def subject_end_operation_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await call.answer()
    await edit_message_text_safe(
        bot=bot,
        text=templates.QUESTION_ADD_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_question_lineup_builder("enter_text"),
    )
    await state.set_state(SubjectStates.enter_test_question_text)


@teacher_user_router.callback_query(
    SubjectStates.press_update_test_title,
    Text(text=["Add-question"]),
    flags=flags,
)
async def subject_end_operation_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await call.answer()
    await edit_message_text_safe(
        bot=bot,
        text=templates.QUESTION_ADD_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_question_lineup_builder("enter_text"),
    )
    await state.set_state(SubjectStates.enter_question_text)


# -------------------Question text enterance-----------------


@teacher_user_router.message(
    SubjectStates.enter_test_question_text,
    flags=flags,
)
async def test_question_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await state.update_data(test_title=message.text.strip())
    await message.delete()

    await edit_message_text_safe(
        bot=bot,
        text=templates.QUESTION_ADD_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_question_lineup_builder(state="enter_text"),
    )
    await state.set_state(SubjectStates.enter_question_text)


@teacher_user_router.message(
    SubjectStates.enter_test_question_text,
    flags=flags,
)
async def test_question_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_TITLE_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_question_lineup_builder(state="enter_text"),
    )


# -------------------Question text enterance-----------------


@teacher_user_router.message(
    SubjectStates.enter_question_text,
    flags=flags,
)
async def text_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(text=message.text.strip())
    state_data = await state.get_data()
    await message.delete()

    def check_question_result_error(result: Union[None, str, Dict]) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result and result != "Timeout":
            errors = get_errors_from_dict(errors_dict=result)
        return errors

    result = await question_creation_request(
        collected_data={
            "text": state_data.get("text"),
            "test": state_data.get("test_title"),
        }
    )

    errors_text = check_question_result_error(result)

    await edit_message_text_safe(
        bot=bot,
        text=templates.QUESTION_TEXT_ENTER_MESSAGE
        if not result
        else templates.ERROR_MESSAGE.format(errors=errors_text),
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_answer_lineup_builder(state="add_answer"),
    )
    if not result:
        await state.set_state(SubjectStates.add_answer)
    else:
        await state.clear()


@teacher_user_router.message(
    SubjectStates.enter_question_text,
    flags=flags,
)
async def text_entering_failed(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.QUESTION_TEXT_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_question_lineup_builder(state="enter_text"),
    )


# -------------------Question mark enterance----------------


# -------------------Question image enterance-----------------
# @teacher_user_router.callback_query(
#     SubjectStates.enter_question_image,
#     Text(text=["Skip"]),
#     flags=flags,
# )
# @teacher_user_router.message(
#     ContentTypeFilter(ContentType.PHOTO),
#     SubjectStates.enter_question_image,
#     flags=flags,
# )
# async def image_entering(message: Message, state: FSMContext, bot: Bot) -> None:
#     state_data = await state.get_data()
#     max_size_photo = max(message.photo, key=lambda photo: photo.file_size)
#     await state.update_data(image=max_size_photo.file_id)
#     await message.delete()
#     await edit_message_text_safe(
#         bot=bot,
#         text=templates.QUESTION_IMAGE_ENTER_MESSAGE,
#         parse_mode=None,
#         chat_id=message.chat.id,
#         message_id=state_data["edit_message_id"],
#         reply_markup=keyboard_question_lineup_builder(state="enter_file"),
#     )
#     await state.set_state(SubjectStates.enter_question_file)


# @teacher_user_router.message(
#     SubjectStates.enter_question_image,
#     flags=flags,
# )
# async def image_entering_failed(message: Message, state: FSMContext, bot: Bot) -> None:
#     state_data = await state.get_data()
#     await message.delete()
#     await edit_message_text_safe(
#         bot=bot,
#         text=templates.QUESTION_IMAGE_ENTER_FAILED_MESSAGE,
#         parse_mode=None,
#         chat_id=message.chat.id,
#         message_id=state_data["edit_message_id"],
#         reply_markup=keyboard_question_lineup_builder(state="enter_image"),
#     )


# -------------------Question file enterance-----------------


# @teacher_user_router.message(
#     SubjectStates.enter_question_file, flags=flags, content_types=ContentType.DOCUMENT
# )
# async def file_entering(message: Message, state: FSMContext, bot: Bot) -> None:
#     document = message.document
#     await state.update_data(file=document.file_id)
#     state_data = await state.get_data()
#     await message.delete()

#     def check_question_result_error(result: Union[None, str, Dict]) -> str:
#         errors = templates.UNTRACKED_ERROR_MESSAGE
#         if result and result != "Timeout":
#             errors = get_errors_from_dict(errors_dict=result)
#         return errors

#     result = await question_creation_request(
#         collected_data={
#             "text": state_data.get("text"),
#             "mark": state_data.get("mark"),
#             "image": state_data.get("image"),
#             "file": state_data.get("file"),
#             "test": state_data.get("test_title"),
#         }
#     )

#     errors_text = check_question_result_error(result)

#     await edit_message_text_safe(
#         bot=bot,
#         text=templates.QUESTION_FILE_ENTER_MESSAGE
#         if not result
#         else templates.ERROR_MESSAGE.format(errors=errors_text),
#         parse_mode=None,
#         chat_id=message.chat.id,
#         message_id=state_data["edit_message_id"],
#         reply_markup=keyboard_answer_lineup_builder(state="add_answer"),
#     )
#     if not result:
#         await state.set_state(SubjectStates.add_answer)
#     else:
#         await state.clear()


# @teacher_user_router.message(
#     SubjectStates.enter_question_file,
#     flags=flags,
# )
# async def image_entering_failed(message: Message, state: FSMContext, bot: Bot) -> None:
#     state_data = await state.get_data()
#     await message.delete()
#     await edit_message_text_safe(
#         bot=bot,
#         text=templates.QUESTION_FILE_ENTER_FAILED_MESSAGE,
#         parse_mode=None,
#         chat_id=message.chat.id,
#         message_id=state_data["edit_message_id"],
#         reply_markup=keyboard_question_lineup_builder(state="enter_file"),
#     )
