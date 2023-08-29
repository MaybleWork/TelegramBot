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
from aiogram.filters.command import Command

import regex
from typing import Any, Dict, Optional, Union

from settings.config import bot_db
from states.result_states import ResultStates
from states.subject_states import SubjectStates
from samples.utils import edit_message_text_safe, get_errors_from_dict
from samples.requests import (
    student_get_request,
    result_student_list_request,
    result_get_request,
    result_teacher_list_request,
    updating_result,
)
from samples import templates
from keyboards.result import keyboard_result_lineup_builder
from keyboards.subject_teacher import keyboard_subject_teacher_lineup_builder


unauthorized_user_router = Router()
unauthorized_user_router.message.filter(NoAuthorizedUserFilter())
teacher_user_router = Router()
teacher_user_router.message.filter(AuthorizedTeacherFilter())
student_user_router = Router()
student_user_router.message.filter(AuthorizedStudentFilter())

flags = {"throttling_key": "default"}


@unauthorized_user_router.message(
    Command("result"),
    flags=flags,
)
async def subject_teacher(
    message: Message,
):
    await message.answer(
        text=templates.UNAUTHORIZED_USER_ACCOUNT_MESSAGE,
    )


@teacher_user_router.message(
    Command("result"),
    flags=flags,
)
async def subject_teacher(
    message: Message,
):
    await message.answer(
        text=templates.TEACHER_MESSAGE,
    )


@student_user_router.message(
    Command("result"),
    flags=flags,
)
async def result_student_command(message: Message, state: FSMContext) -> None:
    answer_msg = await message.answer(
        text=templates.RESULT_STUDENT_STRAT_MESSAGE,
        reply_markup=keyboard_result_lineup_builder("choose_kb"),
    )
    await state.update_data(edit_message_id=answer_msg.message_id)
    await state.set_state(ResultStates.choose_keyboard)


@student_user_router.callback_query(
    ResultStates.choose_keyboard,
    Text(text=["Result-get"]),
    flags=flags,
)
async def result_list_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await call.answer()

    def check_result_error(result: Union[None, str, Dict], key: str = "detail") -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = result.get(key, errors)
        return errors

    statuse_code_stud, response_stud = await student_get_request(
        email=bot_db.get_email_user(user_id=call.from_user.id)
    )

    student_id = response_stud["id"]

    status_code, response = await result_student_list_request(fk=student_id)

    data = [json.loads(json.dumps(obj)) for obj in response]

    formatted_strings = []

    for obj in data:
        name = obj["name"]

        formatted_string = f"Результат: {name}"

        formatted_strings.append(formatted_string)

    result_string = "\n".join(formatted_strings)

    await edit_message_text_safe(
        bot=bot,
        text=templates.RESULT_STUDENT_LIST_START_MESSAGE.format(
            result_string=result_string
        )
        if status_code == 200
        else templates.ERROR_MESSAGE.format(errors=check_result_error(response)),
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_result_lineup_builder(state="get_result"),
    )
    await state.set_state(ResultStates.get_result)


@student_user_router.message(
    ResultStates.get_result,
    (F.text.len() <= 265) & (F.text.len() >= 1),
    flags=flags,
)
async def result_get_message(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(result=message.text.strip())
    state_data = await state.get_data()
    await message.delete()

    statuse_code, response = await result_get_request(name=state_data.get("result"))

    # data = [json.loads(json.dumps(obj)) for obj in response]

    # print(response)
    # print(data)

    formatted_strings = []

    for answer_dict in response["list_answers"]:
        question = answer_dict["question"]["text"]
        mark = answer_dict["mark"]
        formatted_string = f"Питання: {question}, оцінка: {mark}"
        formatted_strings.append(formatted_string)

    result_string = "\n".join(formatted_strings)
    # print(result_string)

    await edit_message_text_safe(
        bot=bot,
        text=templates.RESULT_STUDENT_GET_MESSAGE.format(
            final_mark=response["final_mark"], result_string=result_string
        ),
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_result_lineup_builder(),
    )

    await state.clear()


@student_user_router.message(
    ResultStates.get_result,
    flags=flags,
)
async def result_get_failed(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.RESULT_STUDENT_GET_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_result_lineup_builder(),
    )


# ----------- teach result handler---------------


@teacher_user_router.callback_query(
    SubjectStates.press_update_test_title,
    Text(text=["Result-get"]),
    flags=flags,
)
async def result_list_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await call.answer()

    def check_result_error(result: Union[None, str, Dict], key: str = "detail") -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = result.get(key, errors)
        return errors

    status_code, response = await result_teacher_list_request(
        title=state_data.get("test_title")
    )
    # print(state_data)
    data = [json.loads(json.dumps(obj)) for obj in response]

    formatted_strings = []

    for obj in data:
        name = obj["name"]
        final_mark = obj["final_mark"]

        formatted_string = f"Назва: {name}, оцінка: {final_mark}"

        formatted_strings.append(formatted_string)

    result_string = "\n".join(formatted_strings)

    await edit_message_text_safe(
        bot=bot,
        text=templates.RESULT_TEACHER_START_MESSAGE.format(result_string=result_string)
        if status_code == 200
        else templates.ERROR_MESSAGE.format(errors=check_result_error(response)),
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_teacher_lineup_builder(state="answer"),
    )
    await state.set_state(SubjectStates.enter_result)


# ----------- teach result enter name---------------


@teacher_user_router.message(
    SubjectStates.enter_result,
    (F.text.len() <= 265) & (F.text.len() >= 1),
    flags=flags,
)
async def result_get_message(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(result=message.text.strip())
    state_data = await state.get_data()
    await message.delete()

    statuse_code, response = await result_get_request(name=state_data.get("result"))

    formatted_strings = []

    for answer_dict in response["list_answers"]:
        question = answer_dict["question"]["text"]
        answer_text = answer_dict["text"]
        answer_mark = answer_dict["mark"]
        formatted_string = (
            f"Питання: {question}, відповідь: {answer_text}, оцінка:{answer_mark}"
        )
        formatted_strings.append(formatted_string)

    result_string = "\n".join(formatted_strings)

    await edit_message_text_safe(
        bot=bot,
        text=templates.RESULT_TEACHER_GET_MESSAGE.format(result_string=result_string),
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_teacher_lineup_builder("answer"),
    )
    await state.set_state(SubjectStates.enter_answer)


@teacher_user_router.message(
    SubjectStates.enter_result,
    flags=flags,
)
async def result_get_failed(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.RESULT_TEACHER_GET_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_teacher_lineup_builder(),
    )


# ----------- teach result enter question---------------
@teacher_user_router.callback_query(
    SubjectStates.enter_answer,
    Text(text=["End-account"]),
    flags=flags,
)
async def result_end_operation_callback_query(
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
        reply_markup=keyboard_subject_teacher_lineup_builder(),
    )
    await state.clear()


@teacher_user_router.message(
    SubjectStates.enter_answer,
    (F.text.len() <= 265) & (F.text.len() >= 1),
    flags=flags,
)
async def question_get_message(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(result_question=message.text.strip())
    state_data = await state.get_data()
    await message.delete()

    statuse_code, response = await result_get_request(name=state_data.get("result"))

    formatted_strings = []

    for answer_dict in response["list_answers"]:
        question = answer_dict["question"]["text"]
        answer_text = answer_dict["text"]
        answer_mark = answer_dict["mark"]
        formatted_string = (
            f"Питання: {question}, відповідь: {answer_text}, оцінка:{answer_mark}"
        )
        formatted_strings.append(formatted_string)

    result_string = "\n".join(formatted_strings)

    await edit_message_text_safe(
        bot=bot,
        text=templates.RESULT_TEACHER_QUESTION_MESSAGE.format(
            result_string=result_string
        ),
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_teacher_lineup_builder("enter_title"),
    )
    await state.set_state(SubjectStates.enter_mark)


@teacher_user_router.message(
    SubjectStates.enter_answer,
    flags=flags,
)
async def question_get_failed(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.RESULT_TEACHER_QUESTION_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_teacher_lineup_builder(),
    )


# ----------- teach result enter mark---------------


@teacher_user_router.message(
    SubjectStates.enter_mark,
    (F.text.len() <= 265) & (F.text.len() >= 1),
    flags=flags,
)
async def question_get_message(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(result_mark=message.text.strip())
    state_data = await state.get_data()
    await message.delete()

    statuse_code, response = await result_get_request(name=state_data.get("result"))

    final_mark = response["final_mark"] + int(state_data.get("result_mark"))

    await updating_result(
        upd_data={
            "final_mark": final_mark,
        },
        name=response["name"],
    )

    formatted_strings = []

    for answer_dict in response["list_answers"]:
        question = answer_dict["question"]["text"]
        answer_text = answer_dict["text"]
        answer_mark = answer_dict["mark"]
        formatted_string = (
            f"Питання: {question}, відповідь: {answer_text}, оцінка:{answer_mark}"
        )
        formatted_strings.append(formatted_string)

    result_string = "\n".join(formatted_strings)

    await edit_message_text_safe(
        bot=bot,
        text=templates.RESULT_TEACHER_MARK_MESSAGE.format(result_string=result_string),
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_teacher_lineup_builder("answer"),
    )
    await state.set_state(SubjectStates.enter_answer)


@teacher_user_router.message(
    SubjectStates.enter_mark,
    flags=flags,
)
async def question_get_failed(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.RESULT_TEACHER_MARK_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_teacher_lineup_builder(),
    )
