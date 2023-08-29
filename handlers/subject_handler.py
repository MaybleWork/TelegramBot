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
from states.subject_states import SubjectStates
from samples.utils import edit_message_text_safe, get_errors_from_dict
from samples.requests import (
    teacher_pk_request,
    subject_teacherlist_request,
    subject_create_request,
    student_group_request,
    subject_studentlist_request,
    test_student_list_request,
    test_subject_list_request,
    test_student_get_request,
    updating_test,
)
from samples import templates
from keyboards.subject_teacher import keyboard_subject_teacher_lineup_builder
from keyboards.subject_student import keyboard_subject_student_lineup_builder
from keyboards.question import keyboard_question_lineup_builder
from keyboards.test import keyboard_test_lineup_builder

unauthorized_user_router = Router()
unauthorized_user_router.message.filter(NoAuthorizedUserFilter())
teacher_user_router = Router()
teacher_user_router.message.filter(AuthorizedTeacherFilter())
student_user_router = Router()
student_user_router.message.filter(AuthorizedStudentFilter())

flags = {"throttling_key": "default"}

# -------------------subject_teacher commandhandler-----------------


@unauthorized_user_router.message(
    Command("subjectteach"),
    flags=flags,
)
async def subject_teacher(
    message: Message,
):
    await message.answer(
        text=templates.UNAUTHORIZED_USER_ACCOUNT_MESSAGE,
    )


@student_user_router.message(
    Command("subjectteach"),
    flags=flags,
)
async def subject_teacher(
    message: Message,
):
    await message.answer(
        text=templates.STUDENT_MESSAGE,
    )


@teacher_user_router.message(
    Command("subjectteach"),
    flags=flags,
)
async def subject_teacher_command(message: Message, state: FSMContext) -> None:
    answer_msg = await message.answer(
        text=templates.SUBJECT_TEACHER_STRAT_MESSAGE,
        reply_markup=keyboard_subject_teacher_lineup_builder("choose_keyboard"),
    )
    await state.update_data(edit_message_id=answer_msg.message_id)
    await state.set_state(SubjectStates.choose_keyboard)


@teacher_user_router.callback_query(
    SubjectStates.choose_keyboard,
    Text(text=["Add-test"]),
    flags=flags,
)
async def add_test_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    # print("зайшов")
    state_data = await state.get_data()
    await call.answer()

    def check_teacher_id_result_error(
        result: Union[None, str, Dict], key: str = "detail"
    ) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = result.get(key, errors)
        return errors

    email = bot_db.get_email_user(user_id=call.from_user.id)

    status_code, response = await teacher_pk_request(email=email)

    await state.update_data(teach_fk=response["id"])

    status_code_subj, response__subj = await subject_teacherlist_request(
        fk=response["id"]
    )

    data = [json.loads(json.dumps(obj)) for obj in response__subj]
    # print(response__subj)
    # print(data)

    formatted_strings = []

    for obj in data:
        title = obj["title"]
        formatted_string = f"Назва: {title}"
        formatted_strings.append(formatted_string)

    result_string = "\n".join(formatted_strings)

    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_ADD_SUBJECT_MESSAGE.format(result_string=result_string)
        if status_code == 200
        else templates.ERROR_MESSAGE.format(
            errors=check_teacher_id_result_error(response)
        ),
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_teacher_lineup_builder(state="enter_title"),
    )
    await state.set_state(SubjectStates.enter_test_add_subject_tittle)


@teacher_user_router.message(
    SubjectStates.enter_test_add_subject_tittle,
    (F.text.len() <= 100) & (F.text.len() >= 1),
    flags=flags,
)
async def subject_title_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(title=message.text.strip())
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_ADD_SUBJECT_TITLE_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_teacher_lineup_builder(state="enter_group"),
    )
    await state.set_state(SubjectStates.enter_test_title)


@teacher_user_router.callback_query(
    SubjectStates.choose_keyboard,
    Text(text=["Subject-update"]),
    flags=flags,
)
async def subject_update_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    # print("зайшов")
    state_data = await state.get_data()
    await call.answer()

    def check_teacher_id_result_error(
        result: Union[None, str, Dict], key: str = "detail"
    ) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = result.get(key, errors)
        return errors

    email = bot_db.get_email_user(user_id=call.from_user.id)

    status_code, response = await teacher_pk_request(email=email)

    await state.update_data(teach_fk=response["id"])

    status_code_subj, response__subj = await subject_teacherlist_request(
        fk=response["id"]
    )

    data = [json.loads(json.dumps(obj)) for obj in response__subj]
    # print(response__subj)
    # print(data)

    formatted_strings = []

    for obj in data:
        title = obj["title"]
        formatted_string = f"Назва: {title}"
        formatted_strings.append(formatted_string)

    result_string = "\n".join(formatted_strings)

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_UPDATE_MESSAGE.format(result_string=result_string)
        if status_code == 200
        else templates.ERROR_MESSAGE.format(
            errors=check_teacher_id_result_error(response)
        ),
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_teacher_lineup_builder(state="enter_title"),
    )
    await state.set_state(SubjectStates.enter_update_subject_title)


@teacher_user_router.message(
    SubjectStates.enter_update_subject_title,
    (F.text.len() <= 100) & (F.text.len() >= 1),
    flags=flags,
)
async def subject_title_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(test_title_res=message.text.strip())
    state_data = await state.get_data()
    await message.delete()

    def check_test_result_error(
        result: Union[None, str, Dict], key: str = "detail"
    ) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = result.get(key, errors)
        return errors

    # t = state_data.get("test_title_res")
    # print(t)
    status_code, response = await test_subject_list_request(
        subject=state_data.get("test_title_res")
    )

    data = [json.loads(json.dumps(obj)) for obj in response]
    # print(response)
    # print(data)
    formatted_strings = []

    for obj in data:
        title = obj["title"]

        formatted_string = f"Назва тесту: {title}"

        formatted_strings.append(formatted_string)

    result_string = "\n".join(formatted_strings)

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TITLE_ENTER_MESSAGE.format(
            result_string=result_string
        )
        if status_code == 200
        else templates.ERROR_MESSAGE.format(errors=check_test_result_error(response)),
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_teacher_lineup_builder(state="enter_title"),
    )
    await state.set_state(SubjectStates.enter_update_test_title)


@teacher_user_router.message(
    SubjectStates.enter_update_subject_title,
    flags=flags,
)
async def subject_title_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TITLE_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_teacher_lineup_builder(state="enter_name"),
    )


# -------------------subject enter test title update -----------------
@teacher_user_router.message(
    SubjectStates.enter_update_test_title,
    (F.text.len() <= 100) & (F.text.len() >= 1),
    flags=flags,
)
async def subject_test_title_entering(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    await state.update_data(test_title=message.text.strip())
    state_data = await state.get_data()
    await message.delete()

    # print(state_data)
    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_TITLE_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_teacher_lineup_builder(state="result"),
    )
    await state.set_state(SubjectStates.press_update_test_title)


@teacher_user_router.message(
    SubjectStates.enter_update_test_title,
    flags=flags,
)
async def subject_test_title_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_TITLE_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_teacher_lineup_builder(),
    )


@teacher_user_router.callback_query(
    SubjectStates.press_update_test_title,
    Text(text=["Update-test"]),
    flags=flags,
)
async def subject_update_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    # print("зайшов")
    state_data = await state.get_data()
    await call.answer()

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_UPDATE_START_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )
    await state.set_state(SubjectStates.upd_max_mark)


# -------------------subject enter max mark update -----------------


@teacher_user_router.message(
    SubjectStates.upd_max_mark,
    flags=flags,
)
async def stest_max_mark_entering(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    await state.update_data(upd_max_mark=message.text.strip())
    state_data = await state.get_data()
    await message.delete()

    def check_test_result_error(
        result: Union[None, str, Dict], key: str = "detail"
    ) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = result.get(key, errors)
        return errors

    status_code, response = await updating_test(
        upd_data={"max_mark": state_data.get("upd_max_mark")},
        title=state_data.get("test_title"),
    )

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_MAX_MARK_ENTER_MESSAGE
        if status_code == 200
        else templates.ERROR_MESSAGE.format(errors=check_test_result_error(response)),
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )
    await state.set_state(SubjectStates.upd_number_of_attemps)


@teacher_user_router.message(
    SubjectStates.upd_max_mark,
    flags=flags,
)
async def test_max_mark_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_MAX_MARK_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )


# -------------------subject enter number_of_attemps update -----------------


@teacher_user_router.message(
    SubjectStates.upd_number_of_attemps,
    flags=flags,
)
async def stest_number_of_attemps_entering(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    await state.update_data(upd_number_of_attemps=message.text.strip())
    state_data = await state.get_data()
    await message.delete()

    def check_test_result_error(
        result: Union[None, str, Dict], key: str = "detail"
    ) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = result.get(key, errors)
        return errors

    status_code, response = await updating_test(
        upd_data={"number_of_attemps": state_data.get("upd_number_of_attemps")},
        title=state_data.get("test_title"),
    )

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_NUMBER_OF_ATTEMPS_ENTER_MESSAGE
        if status_code == 200
        else templates.ERROR_MESSAGE.format(errors=check_test_result_error(response)),
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="true_false"),
    )
    await state.set_state(SubjectStates.upd_visibility)


@teacher_user_router.message(
    SubjectStates.upd_number_of_attemps,
    flags=flags,
)
async def test_number_of_attemps_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_NUMBER_OF_ATTEMPS_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )


# -------------------subject enter upd_visibility updat-----------------


@teacher_user_router.callback_query(
    SubjectStates.upd_visibility,
    Text(text=["True"]),
    flags=flags,
)
async def test_true_false_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    await state.update_data(upd_visibility=True)
    state_data = await state.get_data()
    await call.answer()

    status_code, response = await updating_test(
        upd_data={"visibility": state_data.get("upd_visibility")},
        title=state_data.get("test_title"),
    )

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_VISIBILITY_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="true_false"),
    )
    await state.set_state(SubjectStates.upd_automate_checking)


@teacher_user_router.callback_query(
    SubjectStates.upd_visibility,
    Text(text=["False"]),
    flags=flags,
)
async def test_true_false_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    await state.update_data(upd_visibility=False)
    state_data = await state.get_data()
    await call.answer()

    status_code, response = await updating_test(
        upd_data={"visibility": state_data.get("upd_visibility")},
        title=state_data.get("test_title"),
    )

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_VISIBILITY_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="true_false"),
    )
    await state.set_state(SubjectStates.upd_automate_checking)


# -------------------subject enter upd_automate_checking updat-----------------


@teacher_user_router.callback_query(
    SubjectStates.upd_automate_checking,
    Text(text=["True"]),
    flags=flags,
)
async def test_true_false_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    await state.update_data(upd_automate_checking=True)
    state_data = await state.get_data()
    await call.answer()

    status_code, response = await updating_test(
        upd_data={"automate_checking": state_data.get("upd_automate_checking")},
        title=state_data.get("test_title"),
    )

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_AUTO_CHECK_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="true_false"),
    )
    await state.set_state(SubjectStates.upd_question_randomizer)


@teacher_user_router.callback_query(
    SubjectStates.upd_automate_checking,
    Text(text=["False"]),
    flags=flags,
)
async def test_true_false_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    await state.update_data(upd_automate_checking=False)
    state_data = await state.get_data()
    await call.answer()

    status_code, response = await updating_test(
        upd_data={"automate_checking": state_data.get("upd_automate_checking")},
        title=state_data.get("test_title"),
    )

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_AUTO_CHECK_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="true_false"),
    )
    await state.set_state(SubjectStates.upd_question_randomizer)


# -------------------subject enter upd_question_randomizer updat-----------------


@teacher_user_router.callback_query(
    SubjectStates.upd_question_randomizer,
    Text(text=["True"]),
    flags=flags,
)
async def test_true_false_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    await state.update_data(upd_question_randomizer=True)
    state_data = await state.get_data()
    await call.answer()

    status_code, response = await updating_test(
        upd_data={"question_randomizer": state_data.get("upd_question_randomizer")},
        title=state_data.get("test_title"),
    )

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_QUESTION_RANDOMIZER_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="true_false"),
    )
    await state.set_state(SubjectStates.upd_backstep)


@teacher_user_router.callback_query(
    SubjectStates.upd_question_randomizer,
    Text(text=["False"]),
    flags=flags,
)
async def test_true_false_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    await state.update_data(upd_question_randomizer=False)
    state_data = await state.get_data()
    await call.answer()

    status_code, response = await updating_test(
        upd_data={"question_randomizer": state_data.get("upd_question_randomizer")},
        title=state_data.get("test_title"),
    )

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_QUESTION_RANDOMIZER_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="true_false"),
    )
    await state.set_state(SubjectStates.upd_backstep)


# -------------------subject enter upd_backstep updat-----------------


@teacher_user_router.callback_query(
    SubjectStates.upd_backstep,
    Text(text=["True"]),
    flags=flags,
)
async def test_true_false_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    await state.update_data(upd_backstep=True)
    state_data = await state.get_data()
    await call.answer()

    status_code, response = await updating_test(
        upd_data={"backstep": state_data.get("upd_backstep")},
        title=state_data.get("test_title"),
    )

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_BACKSTEP_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )
    await state.set_state(SubjectStates.upd_penalty)


@teacher_user_router.callback_query(
    SubjectStates.upd_backstep,
    Text(text=["False"]),
    flags=flags,
)
async def test_true_false_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    await state.update_data(upd_backstep=False)
    state_data = await state.get_data()
    await call.answer()

    status_code, response = await updating_test(
        upd_data={"backstep": state_data.get("upd_backstep")},
        title=state_data.get("test_title"),
    )

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_BACKSTEP_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )
    await state.set_state(SubjectStates.upd_penalty)


# -------------------subject enter upd_penalty update -----------------


@teacher_user_router.message(
    SubjectStates.upd_penalty,
    flags=flags,
)
async def stest_penalty_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(upd_penalty=message.text.strip())
    state_data = await state.get_data()
    await message.delete()

    def check_test_result_error(
        result: Union[None, str, Dict], key: str = "detail"
    ) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = result.get(key, errors)
        return errors

    status_code, response = await updating_test(
        upd_data={"penalty": state_data.get("upd_penalty")},
        title=state_data.get("test_title"),
    )

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_PENALTY_ENTER_MESSAGE
        if status_code == 200
        else templates.ERROR_MESSAGE.format(errors=check_test_result_error(response)),
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )
    await state.set_state(SubjectStates.upd_level)


@teacher_user_router.message(
    SubjectStates.upd_penalty,
    flags=flags,
)
async def test_penalty_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_PENALTY_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )


# -------------------subject enter upd_level update -----------------


@teacher_user_router.message(
    SubjectStates.upd_level,
    flags=flags,
)
async def stest_level_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(upd_level=message.text.strip())
    state_data = await state.get_data()
    await message.delete()

    def check_test_result_error(
        result: Union[None, str, Dict], key: str = "detail"
    ) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = result.get(key, errors)
        return errors

    status_code, response = await updating_test(
        upd_data={"level": state_data.get("upd_level")},
        title=state_data.get("test_title"),
    )

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_LEVEL_ENTER_MESSAGE
        if status_code == 200
        else templates.ERROR_MESSAGE.format(errors=check_test_result_error(response)),
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )
    await state.set_state(SubjectStates.upd_test_duration)


@teacher_user_router.message(
    SubjectStates.upd_level,
    flags=flags,
)
async def test_level_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_LEVEL_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )


# -------------------subject enter upd_test_duration update -----------------


@teacher_user_router.message(
    SubjectStates.upd_test_duration,
    flags=flags,
)
async def stest_penalty_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(upd_test_duration=message.text.strip())
    state_data = await state.get_data()
    await message.delete()

    def check_test_result_error(
        result: Union[None, str, Dict], key: str = "detail"
    ) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = result.get(key, errors)
        return errors

    status_code, response = await updating_test(
        upd_data={"test_duration": state_data.get("upd_test_duration")},
        title=state_data.get("test_title"),
    )

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_DURATION_ENTER_MESSAGE
        if status_code == 200
        else templates.ERROR_MESSAGE.format(errors=check_test_result_error(response)),
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter_entername"),
    )
    await state.set_state(SubjectStates.upd_start_date)


@teacher_user_router.message(
    SubjectStates.upd_test_duration,
    flags=flags,
)
async def test_penalty_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_DURATION_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )


# -------------------subject enter upd_start_date update -----------------


@teacher_user_router.message(
    SubjectStates.upd_start_date,
    flags=flags,
)
async def stest_penalty_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(upd_start_date=message.text.strip())
    state_data = await state.get_data()
    await message.delete()

    def check_test_result_error(
        result: Union[None, str, Dict], key: str = "detail"
    ) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = result.get(key, errors)
        return errors

    status_code, response = await updating_test(
        upd_data={"start_date": state_data.get("upd_start_date")},
        title=state_data.get("test_title"),
    )

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_START_DATE_ENTER_MESSAGE
        if status_code == 200
        else templates.ERROR_MESSAGE.format(errors=check_test_result_error(response)),
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )
    await state.set_state(SubjectStates.upd_end_date)


# -------------------subject enter upd_end_date update -----------------


@teacher_user_router.message(
    SubjectStates.upd_end_date,
    flags=flags,
)
async def stest_penalty_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(upd_end_date=message.text.strip())
    state_data = await state.get_data()
    await message.delete()

    def check_test_result_error(
        result: Union[None, str, Dict], key: str = "detail"
    ) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = result.get(key, errors)
        return errors

    status_code, response = await updating_test(
        upd_data={"end_date": state_data.get("upd_end_date")},
        title=state_data.get("test_title"),
    )

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_END_DATE_ENTER_MESSAGE
        if status_code == 200
        else templates.ERROR_MESSAGE.format(errors=check_test_result_error(response)),
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )
    await state.set_state(SubjectStates.upd_count_of_question)


@teacher_user_router.message(
    SubjectStates.upd_end_date,
    flags=flags,
)
async def test_penalty_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_END_DATE_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )


# -------------------subject enter upd_count_of_question update -----------------


@teacher_user_router.message(
    SubjectStates.upd_count_of_question,
    flags=flags,
)
async def stest_penalty_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(upd_count_of_question=message.text.strip())
    state_data = await state.get_data()
    await message.delete()

    def check_test_result_error(
        result: Union[None, str, Dict], key: str = "detail"
    ) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = result.get(key, errors)
        return errors

    status_code, response = await updating_test(
        upd_data={"count_of_question": state_data.get("upd_count_of_question")},
        title=state_data.get("test_title"),
    )

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_COUNT_QUEST_ENTER_MESSAGE
        if status_code == 200
        else templates.ERROR_MESSAGE.format(errors=check_test_result_error(response)),
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_question_lineup_builder(state="enter_text"),
    )
    await state.set_state(SubjectStates.enter_question_text)


@teacher_user_router.message(
    SubjectStates.upd_count_of_question,
    flags=flags,
)
async def test_penalty_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_TEST_COUNT_QUEST_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )


# -------------------subject creation -----------------
@teacher_user_router.callback_query(
    SubjectStates.choose_keyboard,
    Text(text=["Subject-creation"]),
    flags=flags,
)
async def subject_creation_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await call.answer()
    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TEACHER_CREATE_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_teacher_lineup_builder(state="enter_title"),
    )
    await state.set_state(SubjectStates.enter_subject_title)


# -------------------subject title enterance-----------------
@teacher_user_router.message(
    SubjectStates.enter_subject_title,
    (F.text.len() <= 100) & (F.text.len() >= 1),
    flags=flags,
)
async def subject_title_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(title=message.text.strip())
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TITLE_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_teacher_lineup_builder(state="enter_group"),
    )
    await state.set_state(SubjectStates.enter_group)


@teacher_user_router.message(
    SubjectStates.enter_subject_title,
    flags=flags,
)
async def subject_title_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TITLE_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_teacher_lineup_builder(state="enter_title"),
    )


# -------------------subject group enterance-----------------


@teacher_user_router.message(
    SubjectStates.enter_group,
    (F.text.len() <= 10) & (F.text.len() >= 1),
    flags=flags,
)
async def subject_title_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(group=message.text.strip())
    await message.delete()

    def check_subject_creation_result_error(result: Union[None, str, Dict]) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result and result != "Timeout":
            errors = get_errors_from_dict(errors_dict=result)
        return errors

    email = bot_db.get_email_user(user_id=message.from_user.id)

    status_code, response = await teacher_pk_request(email=email)

    await state.update_data(teach_fk=response["id"])
    state_data = await state.get_data()

    # print(f"{state_data}")

    result = await subject_create_request(
        collected_data={
            "title": state_data.get("title"),
            "group": state_data.get("group"),
            "teacher": state_data.get("teach_fk"),
        }
    )

    errors_text = check_subject_creation_result_error(result)

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_GROUP_ENTER_MESSAGE
        if not result
        else templates.ERROR_MESSAGE.format(errors=errors_text),
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder("enter_test_title"),
    )

    if not result:
        await state.set_state(SubjectStates.enter_test_title)
    else:
        await state.clear()


@teacher_user_router.message(
    SubjectStates.enter_group,
    flags=flags,
)
async def subject_group_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_GROUP_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_teacher_lineup_builder(state="enter_group"),
    )


# -------------------subject_student commandhandler-----------------


@unauthorized_user_router.message(
    Command("subject_s"),
    flags=flags,
)
async def subject_student(
    message: Message,
):
    await message.answer(
        text=templates.UNAUTHORIZED_USER_ACCOUNT_MESSAGE,
    )


@teacher_user_router.message(
    Command("subject_s"),
    flags=flags,
)
async def subject_student(
    message: Message,
):
    await message.answer(
        text=templates.TEACHER_MESSAGE,
    )


@student_user_router.message(
    Command("subject_s"),
    flags=flags,
)
async def subject_student_command(message: Message, state: FSMContext) -> None:
    answer_msg = await message.answer(
        text=templates.SUBJECT_AUTHORIZED_STUDENT_MESSAGE,
        reply_markup=keyboard_subject_student_lineup_builder(
            "choose_keyboard",
        ),
    )
    await state.update_data(edit_message_id=answer_msg.message_id)
    await state.set_state(SubjectStates.choose_keyboard)


@student_user_router.callback_query(
    SubjectStates.choose_keyboard,
    Text(text=["Group-get"]),
    flags=flags,
)
async def subject_get_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await call.answer()

    def check_student_group_result_error(
        result: Union[None, str, Dict], key: str = "detail"
    ) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = result.get(key, errors)
        return errors

    email = bot_db.get_email_user(user_id=call.from_user.id)

    status_code, response = await student_group_request(email=email)

    await state.update_data(student_group=response["group"])

    status_code_subj, response__subj = await subject_studentlist_request(
        name=response["group"]
    )

    data = [json.loads(json.dumps(obj)) for obj in response__subj]

    formatted_strings = []

    for obj in data:
        title = obj["title"]
        formatted_string = f"Назва: {title}"
        formatted_strings.append(formatted_string)

    result_string = "\n".join(formatted_strings)

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_STUDENT_MESSAGE.format(result_string=result_string)
        if status_code == 200
        else templates.ERROR_MESSAGE.format(
            errors=check_student_group_result_error(response)
        ),
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_student_lineup_builder("enter_test_title"),
    )
    await state.set_state(SubjectStates.student.enter_title)


# -------------------subject student title enterance-----------------


@student_user_router.message(
    SubjectStates.student.enter_title,
    (F.text.len() <= 100) & (F.text.len() >= 1),
    flags=flags,
)
async def student_title_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(s_title=message.text.strip())
    state_data = await state.get_data()
    await message.delete()

    def check_student_title_result_error(
        result: Union[None, str, Dict], key: str = "detail"
    ) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = result.get(key, errors)
        return errors

    status_code, response = await test_student_list_request(
        title=state_data.get("s_title"),
    )

    data = [json.loads(json.dumps(obj)) for obj in response]

    formatted_strings = []

    for obj in data:
        title = obj["title"]

        formatted_string = f"Назва тесту: {title}"

        formatted_strings.append(formatted_string)

    result_string = "\n".join(formatted_strings)

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_STUDENT_TITLE_MESSAGE.format(result_string=result_string)
        if status_code == 200
        else templates.ERROR_MESSAGE.format(
            errors=check_student_title_result_error(response)
        ),
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_student_lineup_builder("enter_test_title"),
    )
    await state.set_state(SubjectStates.student.enter_test_title)


@teacher_user_router.message(
    SubjectStates.enter_group,
    flags=flags,
)
async def student_title_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_TITLE_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_student_lineup_builder(state="enter_test_title"),
    )
