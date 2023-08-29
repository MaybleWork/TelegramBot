import json
from collections import defaultdict

from aiogram import Router, Bot, F
from filters.user import (
    NoAuthorizedUserFilter,
    AuthorizedTeacherFilter,
    AuthorizedStudentFilter,
)
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.filters.state import StateFilter

import datetime
import regex
from typing import Dict, Union

from settings.config import bot_db
from states.subject_states import SubjectStates
from samples.utils import edit_message_text_safe, get_errors_from_dict
from samples.requests import (
    test_creation_request,
    test_student_get_request,
    question_list_request,
    answert_list_request,
    answert_get_request,
    result_get_request,
    updating_result,
    result_creation_request,
    student_get_request,
    result_decrise,
    answert_question_get_request,
    answer_creation_request,
)
from samples import templates
from keyboards.test import keyboard_test_lineup_builder
from keyboards.subject_student import keyboard_subject_student_lineup_builder

unauthorized_user_router = Router()
unauthorized_user_router.message.filter(NoAuthorizedUserFilter())
teacher_user_router = Router()
teacher_user_router.message.filter(AuthorizedTeacherFilter())
student_user_router = Router()
student_user_router.message.filter(AuthorizedStudentFilter())

flags = {"throttling_key": "default"}

# -------------------Test title enterance-----------------


@teacher_user_router.message(
    SubjectStates.enter_test_title,
    (F.text.len() <= 100) & (F.text.len() >= 1),
    flags=flags,
)
async def title_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await state.update_data(test_title=message.text.strip())
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_TITLE_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )
    await state.set_state(SubjectStates.enter_max_mark)


@teacher_user_router.message(
    SubjectStates.enter_test_title,
    flags=flags,
)
async def title_entering_failed(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_TITLE_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )


@teacher_user_router.callback_query(
    SubjectStates.enter_test_title,
    Text(text=["End-test"]),
    flags=flags,
)
async def test_end_operation_callback_query(
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
        reply_markup=keyboard_test_lineup_builder(),
    )
    await state.clear()


# -------------------Test max_mark enterance-----------------


@teacher_user_router.message(
    SubjectStates.enter_max_mark,
    (F.text.regexp(regex.compile(r"^\d+$"))),
    flags=flags,
)
async def max_mark_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await state.update_data(max_mark=message.text.strip())
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_MAX_MARK_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )
    await state.set_state(SubjectStates.enter_number_of_attemps)


@teacher_user_router.message(
    SubjectStates.enter_max_mark,
    flags=flags,
)
async def max_mark_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_MAX_MARK_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )


# -------------------Test number_of_attemps enterance-----------------


@teacher_user_router.message(
    SubjectStates.enter_number_of_attemps,
    (F.text.regexp(regex.compile(r"^\d+$"))),
    flags=flags,
)
async def max_mark_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await state.update_data(number_of_attemps=message.text.strip())
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_NUMBER_OF_ATTEMPS_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="true_false"),
    )
    await state.set_state(SubjectStates.enter_visibility)


@teacher_user_router.message(
    SubjectStates.enter_number_of_attemps,
    flags=flags,
)
async def max_mark_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_NUMBER_OF_ATTEMPS_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )


# -------------------Test visibility enterance-----------------


@teacher_user_router.callback_query(
    SubjectStates.enter_visibility,
    Text(text=["True"]),
    flags=flags,
)
async def test_true_false_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    await state.update_data(visibility=True)
    state_data = await state.get_data()
    await call.answer()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_VISIBILITY_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="true_false"),
    )
    await state.set_state(SubjectStates.enter_automate_checking)


@teacher_user_router.callback_query(
    SubjectStates.enter_visibility,
    Text(text=["False"]),
    flags=flags,
)
async def test_true_false_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    await state.update_data(visibility=False)
    state_data = await state.get_data()
    await call.answer()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_VISIBILITY_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="true_false"),
    )
    await state.set_state(SubjectStates.enter_automate_checking)


# -------------------Test automate_checking enterance-----------------


@teacher_user_router.callback_query(
    SubjectStates.enter_automate_checking,
    Text(text=["True"]),
    flags=flags,
)
async def test_true_false_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    await state.update_data(automate_checking=True)
    state_data = await state.get_data()
    await call.answer()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_AUTOMATE_CHECKING_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="true_false"),
    )
    await state.set_state(SubjectStates.enter_question_randomizer)


@teacher_user_router.callback_query(
    SubjectStates.enter_automate_checking,
    Text(text=["False"]),
    flags=flags,
)
async def test_true_false_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    await state.update_data(automate_checking=False)
    state_data = await state.get_data()
    await call.answer()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_AUTOMATE_CHECKING_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="true_false"),
    )
    await state.set_state(SubjectStates.enter_question_randomizer)


# -------------------Test question_randomizer enterance-----------------


@teacher_user_router.callback_query(
    SubjectStates.enter_question_randomizer,
    Text(text=["True"]),
    flags=flags,
)
async def test_true_false_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    await state.update_data(question_randomizer=True)
    state_data = await state.get_data()
    await call.answer()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_QUESTION_RANDOMIZER_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="true_false"),
    )
    await state.set_state(SubjectStates.enter_backstep)


@teacher_user_router.callback_query(
    SubjectStates.enter_question_randomizer,
    Text(text=["False"]),
    flags=flags,
)
async def test_true_false_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    await state.update_data(question_randomizer=False)
    state_data = await state.get_data()
    await call.answer()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_QUESTION_RANDOMIZER_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="true_false"),
    )
    await state.set_state(SubjectStates.enter_backstep)


# -------------------Test backstep enterance-----------------


@teacher_user_router.callback_query(
    SubjectStates.enter_backstep,
    Text(text=["True"]),
    flags=flags,
)
async def test_true_false_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    await state.update_data(backstep=True)
    state_data = await state.get_data()
    await call.answer()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_BACKSTEP_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )
    await state.set_state(SubjectStates.enter_penalty)


@teacher_user_router.callback_query(
    SubjectStates.enter_backstep,
    Text(text=["False"]),
    flags=flags,
)
async def test_true_false_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    await state.update_data(backstep=False)
    state_data = await state.get_data()
    await call.answer()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_BACKSTEP_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )
    await state.set_state(SubjectStates.enter_penalty)


# -------------------Test penalty enterance-----------------


@teacher_user_router.message(
    SubjectStates.enter_penalty,
    (F.text.regexp(regex.compile(r"^(?:[1-9]|[1-9][0-9]|100)$"))),
    flags=flags,
)
async def penalty_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await state.update_data(penalty=message.text.strip())
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_PENALTY_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )
    await state.set_state(SubjectStates.enter_level)


@teacher_user_router.message(
    SubjectStates.enter_penalty,
    flags=flags,
)
async def penalty_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_PENALTY_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )


# -------------------Test level enterance-----------------


@teacher_user_router.message(
    SubjectStates.enter_level,
    (F.text.regexp(regex.compile(r"^(?:[1-9]|[1-9][0-9]|100)$"))),
    flags=flags,
)
async def level_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await state.update_data(level=message.text.strip())
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_LEVEL_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )
    await state.set_state(SubjectStates.enter_test_duration)


@teacher_user_router.message(
    SubjectStates.enter_level,
    flags=flags,
)
async def level_entering_failed(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_LEVEL_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )


# -------------------Test test_duration enterance-----------------


@teacher_user_router.message(
    SubjectStates.enter_test_duration,
    (F.text.regexp(regex.compile(r"^\d{2}:\d{2}:\d{2}$"))),
    flags=flags,
)
async def test_duration_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await state.update_data(test_duration=message.text.strip())
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_DURATION_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )
    await state.set_state(SubjectStates.enter_start_date)


@teacher_user_router.message(
    SubjectStates.enter_test_duration,
    flags=flags,
)
async def test_duration_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_DURATION_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )


# -------------------Test start_date enterance-----------------


@teacher_user_router.message(
    SubjectStates.enter_start_date,
    (F.text.regexp(regex.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"))),
    flags=flags,
)
async def start_date_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await state.update_data(start_date=message.text.strip())
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_START_DATE_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )
    await state.set_state(SubjectStates.enter_end_date)


@teacher_user_router.message(
    SubjectStates.enter_start_date,
    flags=flags,
)
async def start_date_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_START_DATE_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )


# -------------------Test end_date enterance-----------------


@teacher_user_router.message(
    SubjectStates.enter_end_date,
    (F.text.regexp(regex.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"))),
    flags=flags,
)
async def end_date_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    state_data = await state.get_data()
    await state.update_data(end_date=message.text.strip())
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_END_DATE_ENTER_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )
    await state.set_state(SubjectStates.enter_count_of_question)


@teacher_user_router.message(
    SubjectStates.enter_end_date,
    flags=flags,
)
async def end_date_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_START_DATE_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )


# -------------------Test count_of_question enterance-----------------
@teacher_user_router.message(
    SubjectStates.enter_count_of_question,
    (F.text.regexp(regex.compile(r"^\d+$"))),
    flags=flags,
)
async def count_of_question_entering(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    await state.update_data(count_of_question=message.text.strip())
    state_data = await state.get_data()
    await message.delete()

    def check_test_result_error(result: Union[None, str, Dict]) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result and result != "Timeout":
            errors = get_errors_from_dict(errors_dict=result)
        return errors

    # print(f"{state_data}")
    result = await test_creation_request(
        collected_data={
            "title": state_data.get("test_title"),
            "max_mark": state_data.get("max_mark"),
            "number_of_attemps": state_data.get("number_of_attemps"),
            "visibility": state_data.get("visibility"),
            "automate_checking": state_data.get("automate_checking"),
            "question_randomizer": state_data.get("question_randomizer"),
            "backstep": state_data.get("backstep"),
            "penalty": state_data.get("penalty"),
            "level": state_data.get("level"),
            "test_duration": state_data.get("test_duration"),
            "start_date": state_data.get("start_date"),
            "end_date": state_data.get("end_date"),
            "count_of_question": state_data.get("count_of_question"),
            "subject": state_data.get("title"),
        }
    )

    errors_text = check_test_result_error(result)

    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_COUNT_OF_QUESTION_ENTER_MESSAGE
        if not result
        else templates.ERROR_MESSAGE.format(errors=errors_text),
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(),
    )
    if not result:
        await state.set_state(SubjectStates.enter_question_text)
    else:
        await state.clear()


@teacher_user_router.message(
    SubjectStates.enter_count_of_question,
    flags=flags,
)
async def count_of_question_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.TEST_COUNT_OF_QUESTION_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_test_lineup_builder(state="enter"),
    )


# -------------------Student test get-----------------


@student_user_router.message(
    SubjectStates.student.enter_test_title,
    (F.text.len() <= 100) & (F.text.len() >= 1),
    flags=flags,
)
async def student_test_get(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(student_test_title=message.text.strip())
    state_data = await state.get_data()
    await message.delete()

    def check_test_student_result_error(
        result: Union[None, str, Dict], key: str = "detail"
    ) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = result.get(key, errors)
        return errors

    status_code, response = await test_student_get_request(
        title=state_data.get("student_test_title")
    )
    # student_name = bot_db.get_full_name_user(user_id=message.from_user.id)

    # test_name = state_data.get("student_test_title")
    # statuse_code_res, response_res = await result_get_request(
    #     name=f"{student_name}:{test_name}"
    # )
    await state.update_data(student_final_mark=0)

    await state.update_data(student_test_max_mark=response["max_mark"])
    await state.update_data(
        student_test_number_of_attemps=response["number_of_attemps"]
    )
    await state.update_data(
        student_test_automate_checking=response["automate_checking"]
    )
    await state.update_data(student_test_backstep=response["backstep"])
    await state.update_data(student_test_penalty=response["penalty"])
    await state.update_data(student_test_level=response["level"])
    hours, minutes, seconds = map(int, response["test_duration"].split(":"))
    duration = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
    await state.update_data(student_test_test_duration=duration)
    await state.update_data(student_start_test_data=datetime.datetime.now())

    question_text, question_id, question_data = await send_current_question(
        message.chat.id, state_data.get("student_test_title"), 1, bot
    )
    # await state.update_data(student_question_mark=question_mark)

    answ_status_code, answ_response = await answert_list_request(text=question_text)

    if answ_response[0]["is_test"] == True or answ_response[0]["is_multitest"] == True:
        data = [json.loads(json.dumps(obj)) for obj in answ_response]

        formatted_strings = []

        for obj in data:
            text = obj["text"]

            formatted_string = f"Відповіді: {text},"

            formatted_strings.append(formatted_string)

        result_string = "\n".join(formatted_strings)
    else:
        result_string = "Відкрита відповідь"

    # print(result_string)
    student_name = bot_db.get_full_name_user(user_id=message.from_user.id)

    test_name = state_data.get("student_test_title")

    statuse_code_res, response_res = await result_get_request(
        name=f"{student_name}:{test_name}"
    )

    if statuse_code_res == 200:
        if response_res["number_of_attemps"] == 0:
            await edit_message_text_safe(
                bot=bot,
                text=templates.SUBJECT_STUDENT_TEST_TITLE_ENTER_FAILED_MESSAGE,
                parse_mode=None,
                chat_id=message.chat.id,
                message_id=state_data["edit_message_id"],
                reply_markup=keyboard_subject_student_lineup_builder(),
            )
        else:
            await edit_message_text_safe(
                bot=bot,
                text=templates.SUBJECT_STUDENT_TITLE_ENTER_MESSAGE.format(
                    question_text=question_text, result_string=result_string
                ),
                parse_mode=None,
                chat_id=message.chat.id,
                message_id=state_data["edit_message_id"],
                reply_markup=keyboard_subject_student_lineup_builder(
                    "send_answer", question_data, response["backstep"]
                ),
            )
        if response_res["number_of_attemps"] == 0:
            await state.clear()
        else:
            await state.set_state(SubjectStates.student.send_answer)
    else:
        await edit_message_text_safe(
            bot=bot,
            text=templates.SUBJECT_STUDENT_TITLE_ENTER_MESSAGE.format(
                question_text=question_text, result_string=result_string
            ),
            parse_mode=None,
            chat_id=message.chat.id,
            message_id=state_data["edit_message_id"],
            reply_markup=keyboard_subject_student_lineup_builder(
                "send_answer", question_data, response["backstep"]
            ),
        )
        await state.set_state(SubjectStates.student.send_answer)


@student_user_router.message(
    SubjectStates.student.enter_test_title,
    flags=flags,
)
async def student_test_get_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_STUDENT_TITLE_ENTER_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_student_lineup_builder(state="enter_test_title"),
    )


# -------------------Student test start-----------------

pages_cache = defaultdict(dict)


async def send_current_question(chat_id, title, page, bot: Bot):
    if page not in pages_cache[chat_id]:
        question_data = await question_list_request(title, page)
        if question_data is None or not question_data["results"]:
            await bot.send_message(
                chat_id,
                templates.NO_FOUND_ERROR,
                parse_mode=None,
            )
            return
        pages_cache[chat_id][page] = question_data
    else:
        question_data = pages_cache[chat_id][page]

    results_dict = question_data["results"][0]
    question_text = results_dict["text"]
    question_id = results_dict["id"]

    return question_text, question_id, question_data
    # if edit_message_id is None:
    #     await bot.send_message(
    #         chat_id,
    #         question_text,
    #         parse_mode="MarkdownV2",
    #         reply_markup=inline_kb_builder.as_markup(),
    #     )
    # else:
    #     await edit_message_text_safe(
    #         bot=bot,
    #         text=question_text,
    #         parse_mode="MarkdownV2",
    #         chat_id=chat_id,
    #         message_id=edit_message_id,
    #         reply_markup=inline_kb_builder.as_markup(),
    #     )


# -------------------Student test start keyboard-----------------
@student_user_router.callback_query(
    SubjectStates.student.send_answer,
    Text(text=["Previous"]),
    flags=flags,
)
async def test_previous_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    if state_data.get("get_page") == None:
        await state.update_data(get_page=1 - 1)
    else:
        await state.update_data(get_page=int(state_data.get("get_page")) - 1)
    state_data = await state.get_data()
    question_text, question_id, question_data = await send_current_question(
        call.message.chat.id,
        state_data.get("student_test_title"),
        state_data.get("get_page"),
        bot,
    )
    # await state.update_data(student_question_mark=question_mark)

    status_code, response = await answert_list_request(text=question_text)

    if response[0]["is_test"] == True or response[0]["is_multitest"] == True:
        data = [json.loads(json.dumps(obj)) for obj in response]

        formatted_strings = []

        for obj in data:
            text = obj["text"]

            formatted_string = f"Відповіді: {text},"

            formatted_strings.append(formatted_string)

        result_string = "\n".join(formatted_strings)
    else:
        result_string = "Відкрита відповідь"

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_STUDENT_TITLE_ENTER_MESSAGE.format(
            question_text=question_text, result_string=result_string
        ),
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_student_lineup_builder(
            "send_answer", question_data, state_data.get("student_test_backstep")
        ),
    )

    if (
        state_data.get("student_start_test_data")
        + state_data.get("student_test_test_duration")
        < datetime.datetime.now()
    ):
        await state.set_state(SubjectStates.student.end_test)
    else:
        await state.set_state(SubjectStates.student.send_answer)


@student_user_router.callback_query(
    SubjectStates.student.send_answer,
    Text(text=["Next"]),
    flags=flags,
)
async def test_next_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    if state_data.get("get_page") == None:
        await state.update_data(get_page=1 + 1)
    else:
        await state.update_data(get_page=int(state_data.get("get_page")) + 1)
    state_data = await state.get_data()
    question_text, question_id, question_data = await send_current_question(
        call.message.chat.id,
        state_data.get("student_test_title"),
        state_data.get("get_page"),
        bot,
    )
    # await state.update_data(student_question_mark=question_mark)

    status_code, response = await answert_list_request(text=question_text)
    # print(response)

    if response[0]["is_test"] == True or response[0]["is_multitest"] == True:
        data = [json.loads(json.dumps(obj)) for obj in response]

        formatted_strings = []

        for obj in data:
            text = obj["text"]

            formatted_string = f"Відповіді: {text},"

            formatted_strings.append(formatted_string)

        result_string = "\n".join(formatted_strings)
    else:
        result_string = "Відкрита відповідь"

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_STUDENT_TITLE_ENTER_MESSAGE.format(
            question_text=question_text, result_string=result_string
        ),
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_student_lineup_builder(
            "send_answer", question_data, state_data.get("student_test_backstep")
        ),
    )

    if (
        state_data.get("student_start_test_data")
        + state_data.get("student_test_test_duration")
        < datetime.datetime.now()
    ):
        await state.set_state(SubjectStates.student.end_test)
    else:
        await state.set_state(SubjectStates.student.send_answer)


@student_user_router.callback_query(
    StateFilter(*[SubjectStates.student.send_answer, SubjectStates.student.end_test]),
    Text(text=["Test-end"]),
    flags=flags,
)
async def Test_end_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await call.answer()

    student_name = bot_db.get_full_name_user(user_id=call.from_user.id)

    test_name = state_data.get("student_test_title")

    statuse_code_res, response_res = await result_get_request(
        name=f"{student_name}:{test_name}"
    )
    level = state_data.get("student_test_max_mark") * (
        state_data.get("student_test_level") / 100
    )
    # print(level)
    # print(response_res["final_mark"])
    if response_res["final_mark"] < level:
        final_mark = 0
    else:
        final_mark = response_res["final_mark"]

    await updating_result(
        upd_data={"final_mark": final_mark}, name=response_res["name"]
    )

    await result_decrise(
        name=response_res["name"], title=state_data.get("student_test_title")
    )

    await edit_message_text_safe(
        bot=bot,
        text=templates.GROUP_END_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_student_lineup_builder(),
    )
    await state.clear()


@student_user_router.message(
    SubjectStates.student.send_answer,
    (F.text.len() <= 265) & (F.text.len() >= 1),
    flags=flags,
)
async def student_send_answer(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(student_send_answer=message.text.strip())
    state_data = await state.get_data()
    if state_data.get("get_page") == None:
        await state.update_data(get_page=1)
        state_data = await state.get_data()
    else:
        state_data.get("get_page")
        state_data = await state.get_data()
    await message.delete()
    # print(state_data)
    question_text, question_id, question_data = await send_current_question(
        message.chat.id,
        state_data.get("student_test_title"),
        state_data.get("get_page"),
        bot,
    )

    status_code, response = await answert_list_request(text=question_text)
    # print(response)
    # print(response)
    if response[0]["is_test"] == True or response[0]["is_multitest"] == True:
        data = [json.loads(json.dumps(obj)) for obj in response]

        formatted_strings = []

        for obj in data:
            text = obj["text"]

            formatted_string = f"Відповіді: {text},"

            formatted_strings.append(formatted_string)

        result_string = "\n".join(formatted_strings)
    else:
        result_string = "Відкрита відповідь"

    # print(result_string)

    if response[0]["is_text"] == True:
        statuse_code_answ_q, response_answ_q = await answert_question_get_request(
            question=question_text
        )

        if statuse_code_answ_q == 200:
            stat, resp = await answer_creation_request(
                collected_data={
                    "is_text": True,
                    "text": state_data.get("student_send_answer"),
                    "mark": response_answ_q[0]["mark"],
                    "question": question_text,
                }
            )

        statuse_code_answ, response_answ = await answert_get_request(
            text=state_data.get("student_send_answer")
        )
    else:
        statuse_code_answ, response_answ = await answert_get_request(
            text=state_data.get("student_send_answer")
        )

    student_name = bot_db.get_full_name_user(user_id=message.from_user.id)

    test_name = state_data.get("student_test_title")

    statuse_code_res, response_res = await result_get_request(
        name=f"{student_name}:{test_name}"
    )

    statuse_code_stud, response_stud = await student_get_request(
        email=bot_db.get_email_user(user_id=message.from_user.id)
    )

    noted_answer = {}

    if (
        response_answ["id"] in noted_answer.values()
        and question_id in noted_answer.keys()
    ):
        pass
    elif (
        response_answ["id"] not in noted_answer.values()
        and question_id in noted_answer.keys()
        and response_answ["is_multitest"] == True
    ):
        if state_data.get("list_answers") == None:
            await state.update_data(list_answers=[response_answ["id"]])
            state_data = await state.get_data()

        else:
            lst = state_data.get("list_answers")
            lst.append(response_answ["id"])
            await state.update_data(list_answers=lst)
            state_data = await state.get_data()

    else:
        if state_data.get("list_answers") == None:
            await state.update_data(list_answers=[response_answ["id"]])
            state_data = await state.get_data()

        else:
            lst = state_data.get("list_answers")
            lst.append(response_answ["id"])
            await state.update_data(list_answers=lst)
            state_data = await state.get_data()

    student_id = response_stud["id"]
    number = state_data.get("student_test_number_of_attemps")
    # print(number)
    # print(response_res["number_of_attemps"])

    if statuse_code_res == 200:
        if (
            state_data.get("student_test_number_of_attemps")
            > response_res["number_of_attemps"]
            and state_data.get("automate_checking") == False
        ):
            # and state_data.get("automate_checking") == True

            # print("Зайшов")
            answer_mark = 0
        elif (
            state_data.get("student_test_number_of_attemps")
            > response_res["number_of_attemps"]
        ):
            answer_mark = response_answ["mark"] * (
                1 - (state_data.get("student_test_penalty") / 100)
            )
        else:
            # print("Зайшов 2")
            answer_mark = response_answ["mark"]

        if state_data.get("mark_list") == None:
            await state.update_data(mark_list=[answer_mark])
            state_data = await state.get_data()
            final_mark = sum(state_data.get("mark_list"))

        else:
            mrk = state_data.get("mark_list")
            mrk.append(answer_mark)
            await state.update_data(mark_list=mrk)
            state_data = await state.get_data()
            final_mark = sum(state_data.get("mark_list"))

    # print(final_mark)
    # final_mark = sum(state_data.get("mark_list"))
    # print(state_data)
    if statuse_code_res == 200:
        await updating_result(
            upd_data={
                "list_answers": state_data.get("list_answers"),
                "final_mark": final_mark,
                "number_of_attemps": response_res["number_of_attemps"],
            },
            name=response_res["name"],
        )
    elif statuse_code_res == 200:
        pass
    else:
        await result_creation_request(
            collected_data={
                "name": f"{student_name}:{test_name}",
                "list_answers": response_answ["id"],
                "final_mark": response_answ["mark"],
                "number_of_attemps": state_data.get("student_test_number_of_attemps"),
                "student": student_id,
                "test": test_name,
            }
        )

    # await state.update_data(student_question_mark=question_mark)

    await edit_message_text_safe(
        bot=bot,
        text=templates.SUBJECT_STUDENT_ANSWER_ENTER_MESSAGE.format(
            question_text=question_text, result_string=result_string
        ),
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_subject_student_lineup_builder(
            "send_answer", question_data, state_data.get("student_test_backstep")
        ),
    )
    data = state_data.get("student_start_test_data") + state_data.get(
        "student_test_test_duration"
    )
    if (
        state_data.get("student_start_test_data")
        + state_data.get("student_test_test_duration")
        < datetime.datetime.now()
    ):
        await state.set_state(SubjectStates.student.end_test)
    else:
        await state.set_state(SubjectStates.student.send_answer)
