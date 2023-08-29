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
from aiogram.filters.state import StateFilter


import regex
from typing import Dict, Union

from states.subject_states import SubjectStates
from samples.utils import edit_message_text_safe, get_errors_from_dict
from samples.requests import answer_creation_request
from samples import templates
from keyboards.answer import keyboard_answer_lineup_builder
from keyboards.question import keyboard_question_lineup_builder

unauthorized_user_router = Router()
unauthorized_user_router.message.filter(NoAuthorizedUserFilter())
teacher_user_router = Router()
teacher_user_router.message.filter(AuthorizedTeacherFilter())
student_user_router = Router()
student_user_router.message.filter(AuthorizedStudentFilter())

flags = {"throttling_key": "default"}


@teacher_user_router.callback_query(
    StateFilter(
        *[
            SubjectStates.enter_test_answer_text,
            SubjectStates.enter_multitest_answer_text,
        ]
    ),
    Text(text=["Question-add"]),
    flags=flags,
)
async def Test_question_callback_query(
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
        reply_markup=keyboard_question_lineup_builder(state="enter_text"),
    )
    await state.set_state(SubjectStates.enter_question_text)


@teacher_user_router.callback_query(
    SubjectStates.add_answer,
    Text(text=["Test-answer"]),
    flags=flags,
)
async def Test_answer_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await call.answer()
    await edit_message_text_safe(
        bot=bot,
        text=templates.ANSWER_TEST_START_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_answer_lineup_builder(state="test_enterance"),
    )
    await state.set_state(SubjectStates.enter_test_answer_text)


@teacher_user_router.callback_query(
    SubjectStates.add_answer,
    Text(text=["Multitest-answer"]),
    flags=flags,
)
async def Multitest_answer_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await call.answer()
    await edit_message_text_safe(
        bot=bot,
        text=templates.ANSWER_MULTITEST_START_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_answer_lineup_builder(state="test_enterance"),
    )
    await state.set_state(SubjectStates.enter_multitest_answer_text)


@teacher_user_router.callback_query(
    SubjectStates.add_answer,
    Text(text=["Text-answer"]),
    flags=flags,
)
async def Text_answer_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await call.answer()

    def check_answer_result_error(result: Union[None, str, Dict]) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = get_errors_from_dict(errors_dict=result)
        return errors

    status_code, response = await answer_creation_request(
        collected_data={"is_text": True, "question": state_data.get("text")}
    )
    errors_text = check_answer_result_error(response)

    await edit_message_text_safe(
        bot=bot,
        text=templates.ANSWER_MULTITEST_TEST_TEXT_MESSAGE
        if status_code == 201
        else templates.ERROR_MESSAGE.format(errors=errors_text),
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_question_lineup_builder(state="enter_max_mark"),
    )
    await state.set_state(SubjectStates.enter_text_answer_mark)


# -------------------Text answer mark enterance-----------------


@teacher_user_router.message(
    SubjectStates.enter_text_answer_mark,
    (F.text.regexp(regex.compile(r"^\d+$"))),
    flags=flags,
)
async def mark_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(mark=message.text.strip())
    state_data = await state.get_data()
    await message.delete()

    def check_answer_result_error(result: Union[None, str, Dict]) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = get_errors_from_dict(errors_dict=result)
        return errors

    status_code, response = await answer_creation_request(
        collected_data={
            "is_text": True,
            "mark": state_data.get("mark"),
            "question": state_data.get("text"),
        }
    )
    errors_text = check_answer_result_error(response)

    await edit_message_text_safe(
        bot=bot,
        text=templates.ANSWER_TEXT_START_MESSAGE
        if status_code == 201
        else templates.ERROR_MESSAGE.format(errors=errors_text),
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_question_lineup_builder(state="enter_text"),
    )
    await state.set_state(SubjectStates.enter_question_text)


@teacher_user_router.message(
    SubjectStates.enter_text_answer_mark,
    flags=flags,
)
async def mark_entering_failed(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.ANSWER_TEST_MARK_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_question_lineup_builder(state="enter_max_mark"),
    )


# -------------------Test answer text enterance-----------------


@teacher_user_router.message(
    SubjectStates.enter_test_answer_text,
    (F.text.len() <= 265) & (F.text.len() >= 1),
    flags=flags,
)
async def answer_text_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await state.update_data(answer_text=message.text.strip())
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.ANSWER_TEST_TEXT_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_answer_lineup_builder(state="mark_enterance"),
    )
    await state.set_state(SubjectStates.enter_test_mark)


@teacher_user_router.message(
    SubjectStates.enter_test_answer_text,
    flags=flags,
)
async def answer_text_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.ANSWER_TEST_TEXT_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_answer_lineup_builder(state="test_start"),
    )


@teacher_user_router.message(
    SubjectStates.enter_test_mark,
    F.text.regexp(regex.compile(r"^\d+$")),
    flags=flags,
)
async def mark_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(mark=message.text.strip())
    state_data = await state.get_data()
    await message.delete()

    await edit_message_text_safe(
        bot=bot,
        text=templates.ANSWER_TEST_MARK_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_answer_lineup_builder(state="true_false"),
    )
    await state.set_state(SubjectStates.enter_test_answer_is_correct)


@teacher_user_router.message(
    SubjectStates.enter_test_mark,
    flags=flags,
)
async def mark_entering_failed(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.ANSWER_TEST_MARK_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_question_lineup_builder(state="enter_max_mark"),
    )


# -------------------Test answer is_correct enterance-----------------
@teacher_user_router.callback_query(
    SubjectStates.enter_test_answer_is_correct,
    Text(text=["True"]),
    flags=flags,
)
async def answer_true_false_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    await state.update_data(is_correact=True)
    state_data = await state.get_data()
    await call.answer()

    def check_answer_result_error(result: Union[None, str, Dict]) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = get_errors_from_dict(errors_dict=result)
        return errors

    status_code, response = await answer_creation_request(
        collected_data={
            "is_test": True,
            "text": state_data.get("answer_text"),
            "is_correct": True,
            "mark": state_data.get("mark"),
            "question": state_data.get("text"),
        }
    )
    errors_text = check_answer_result_error(response)

    await edit_message_text_safe(
        bot=bot,
        text=templates.ANSWER_TEST_IS_CORRECT_MESSAGE
        if status_code == 201
        else templates.ERROR_MESSAGE.format(errors=errors_text),
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_answer_lineup_builder(state="test_enterance"),
    )
    await state.set_state(SubjectStates.enter_test_answer_text)


@teacher_user_router.callback_query(
    SubjectStates.enter_test_answer_is_correct,
    Text(text=["False"]),
    flags=flags,
)
async def answer_true_false_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    await state.update_data(is_correact=False)
    state_data = await state.get_data()
    await call.answer()

    def check_answer_result_error(result: Union[None, str, Dict]) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = get_errors_from_dict(errors_dict=result)
        return errors

    status_code, response = await answer_creation_request(
        collected_data={
            "is_test": True,
            "text": state_data.get("answer_text"),
            "is_correct": False,
            "question": state_data.get("text"),
        }
    )
    errors_text = check_answer_result_error(response)

    await edit_message_text_safe(
        bot=bot,
        text=templates.ANSWER_TEST_IS_CORRECT_MESSAGE
        if status_code == 201
        else templates.ERROR_MESSAGE.format(errors=errors_text),
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_answer_lineup_builder(state="test_enterance"),
    )
    await state.set_state(SubjectStates.enter_test_answer_text)


# -------------------Multitest answer text enterance-----------------
@teacher_user_router.message(
    SubjectStates.enter_multitest_answer_text,
    (F.text.len() <= 265) & (F.text.len() >= 1),
    flags=flags,
)
async def answer_text_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await state.update_data(answer_text=message.text.strip())
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.ANSWER_MULTITEST_TEST_TEXT_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_answer_lineup_builder(state="test_enterance"),
    )
    await state.set_state(SubjectStates.enter_multitest_mark)


@teacher_user_router.message(
    SubjectStates.enter_multitest_answer_text,
    flags=flags,
)
async def answer_text_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.ANSWER_TEST_TEXT_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_answer_lineup_builder(state="test_enterance"),
    )


# -------------------Multitest answer mark enterance-----------------


@teacher_user_router.message(
    SubjectStates.enter_multitest_mark,
    F.text.regexp(regex.compile(r"^\d+$")),
    flags=flags,
)
async def answer_mark_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await state.update_data(answer_mark=message.text.strip())
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.ANSWER_TEST_MARK_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_answer_lineup_builder(state="true_false"),
    )
    await state.set_state(SubjectStates.enter_multitest_is_correct)


@teacher_user_router.message(
    SubjectStates.enter_multitest_mark,
    flags=flags,
)
async def mark_entering_failed(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.ANSWER_TEST_MARK_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_answer_lineup_builder(),
    )


# -------------------Multitest answer is_correct enterance-----------------


@teacher_user_router.callback_query(
    SubjectStates.enter_multitest_is_correct,
    Text(text=["True"]),
    flags=flags,
)
async def answer_true_false_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    await state.update_data(is_correact=True)
    state_data = await state.get_data()
    await call.answer()

    def check_answer_result_error(result: Union[None, str, Dict]) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = get_errors_from_dict(errors_dict=result)
        return errors

    status_code, response = await answer_creation_request(
        collected_data={
            "is_multitest": True,
            "text": state_data.get("answer_text"),
            "is_correct": True,
            "mark": state_data.get("answer_mark"),
            "question": state_data.get("text"),
        }
    )
    errors_text = check_answer_result_error(response)

    await edit_message_text_safe(
        bot=bot,
        text=templates.ANSWER_TEST_IS_CORRECT_MESSAGE
        if status_code == 201
        else templates.ERROR_MESSAGE.format(errors=errors_text),
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_answer_lineup_builder(state="test_enterance"),
    )
    await state.set_state(SubjectStates.enter_multitest_answer_text)


@teacher_user_router.callback_query(
    SubjectStates.enter_multitest_is_correct,
    Text(text=["False"]),
    flags=flags,
)
async def answer_true_false_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    await state.update_data(is_correact=False)
    state_data = await state.get_data()
    await call.answer()

    def check_answer_result_error(result: Union[None, str, Dict]) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = get_errors_from_dict(errors_dict=result)
        return errors

    status_code, response = await answer_creation_request(
        collected_data={
            "is_multitest": True,
            "text": state_data.get("answer_text"),
            "is_correct": False,
            "mark": state_data.get("answer_mark"),
            "question": state_data.get("text"),
        }
    )
    errors_text = check_answer_result_error(response)

    await edit_message_text_safe(
        bot=bot,
        text=templates.ANSWER_TEST_IS_CORRECT_MESSAGE
        if status_code == 201
        else templates.ERROR_MESSAGE.format(errors=errors_text),
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_answer_lineup_builder(state="test_enterance"),
    )
    await state.set_state(SubjectStates.enter_multitest_answer_text)
