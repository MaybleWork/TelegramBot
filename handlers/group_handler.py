from aiogram import Router, Bot, F
from filters.user import (
    EmailFilter,
    NoAuthorizedUserFilter,
    AuthorizedTeacherFilter,
    AuthorizedStudentFilter,
)
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command

import json
import regex
from typing import Dict, Union

from states.group_states import GroupStates
from settings.config import bot_db
from samples import templates
from samples.utils import edit_message_text_safe, get_errors_from_dict
from keyboards.group import keyboard_group_lineup_builder
from samples.requests import (
    student_all_list_request,
    add_student_to_group,
    group_all_list_request,
    group_update_request,
    group_create_request,
)

unauthorized_user_router = Router()
unauthorized_user_router.message.filter(NoAuthorizedUserFilter())
teacher_user_router = Router()
teacher_user_router.message.filter(AuthorizedTeacherFilter())
student_user_router = Router()
student_user_router.message.filter(AuthorizedStudentFilter())

flags = {"throttling_key": "default"}


@unauthorized_user_router.message(
    Command("group"),
    flags=flags,
)
async def user_group(
    message: Message,
):
    await message.answer(
        text=templates.UNAUTHORIZED_USER_GROUP_MESSAGE,
    )


@student_user_router.message(
    Command("group"),
    flags=flags,
)
async def user_group(
    message: Message,
):
    await message.answer(
        text=templates.STUDENT_MESSAGE,
    )


@teacher_user_router.message(
    Command("group"),
    flags=flags,
)
async def user_group(message: Message, state: FSMContext) -> None:
    answer_msg = await message.answer(
        text=templates.TEACHER_GROUP_MESSAGE,
        reply_markup=keyboard_group_lineup_builder("choose_keyboard"),
    )
    await state.update_data(edit_message_id=answer_msg.message_id)
    await state.set_state(GroupStates.choose_keyboard)


@teacher_user_router.callback_query(
    GroupStates.choose_keyboard,
    Text(text=["Group-creation"]),
    flags=flags,
)
async def group_creation_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await call.answer()
    await edit_message_text_safe(
        bot=bot,
        text=templates.GROUP_START_MESSAGE,
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_group_lineup_builder(state="enter_name"),
    )
    await state.set_state(GroupStates.enter_name)


@teacher_user_router.callback_query(
    GroupStates.choose_keyboard,
    Text(text=["Student-add"]),
    flags=flags,
)
async def student_add_group_callback_query(
    call: CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await call.answer()

    def check_group_result_error(
        result: Union[None, str, Dict], key: str = "detail"
    ) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = result.get(key, errors)
        return errors

    status_code, response = await group_all_list_request()

    data = [json.loads(json.dumps(obj)) for obj in response]

    formatted_strings = []

    for obj in data:
        name = obj["name"]

        formatted_string = f"Назва групи: {name}"

        formatted_strings.append(formatted_string)

    result_string = "\n".join(formatted_strings)

    await edit_message_text_safe(
        bot=bot,
        text=templates.GROUP_ADD_STUDENT_START_MESSAGE.format(
            result_string=result_string
        )
        if status_code == 200
        else templates.ERROR_MESSAGE.format(errors=check_group_result_error(response)),
        parse_mode=None,
        chat_id=call.message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_group_lineup_builder(state="enter_name"),
    )
    await state.set_state(GroupStates.enter_name)


# @teacher_user_router.callback_query(
#     GroupStates.choose_keyboard,
#     Text(text=["Group-update"]),
#     flags=flags,
# )
# async def group_update_callback_query(
#     call: CallbackQuery, state: FSMContext, bot: Bot
# ) -> None:
#     state_data = await state.get_data()
#     await call.answer()

#     def check_group_result_error(
#         result: Union[None, str, Dict], key: str = "detail"
#     ) -> str:
#         errors = templates.UNTRACKED_ERROR_MESSAGE
#         if result == "Timeout":
#             errors = result.get(key, errors)
#         return errors

#     status_code, response = await group_all_list_request()

#     data = [json.loads(json.dumps(obj)) for obj in response]

#     formatted_strings = []

#     for obj in data:
#         name = obj["name"]

#         formatted_string = f"Назва групи: {name}"

#         formatted_strings.append(formatted_string)

#     result_string = "\n".join(formatted_strings)

#     await edit_message_text_safe(
#         bot=bot,
#         text=templates.GROUP_UPDATE_START_MESSAGE.format(result_string=result_string)
#         if status_code == 200
#         else templates.ERROR_MESSAGE.format(errors=check_group_result_error(response)),
#         parse_mode=None,
#         chat_id=call.message.chat.id,
#         message_id=state_data["edit_message_id"],
#         reply_markup=keyboard_group_lineup_builder(state="enter_name"),
#     )
#     await state.set_state(GroupStates.update.enter_name)


# # -------------------group enter_name update-----------------


# @teacher_user_router.message(
#     GroupStates.update.enter_name,
#     (F.text.len() <= 10) & (F.text.len() >= 1),
#     flags=flags,
# )
# async def group_name_update_entering(
#     message: Message, state: FSMContext, bot: Bot
# ) -> None:
#     state_data = await state.get_data()
#     await state.update_data(name=message.text.strip())
#     await message.delete()

#     await edit_message_text_safe(
#         bot=bot,
#         text=templates.GROUP_NAME_UPDATE_MESSAGE,
#         parse_mode=None,
#         chat_id=message.chat.id,
#         message_id=state_data["edit_message_id"],
#         reply_markup=keyboard_group_lineup_builder(state="update_name"),
#     )
#     await state.set_state(GroupStates.update.update_name)


# @teacher_user_router.message(
#     GroupStates.update.enter_name,
#     flags=flags,
# )
# async def group_name_update_entering_failed(
#     message: Message, state: FSMContext, bot: Bot
# ) -> None:
#     state_data = await state.get_data()
#     await message.delete()
#     await edit_message_text_safe(
#         bot=bot,
#         text=templates.GROUP_NAME_FAILED_MESSAGE,
#         parse_mode=None,
#         chat_id=message.chat.id,
#         message_id=state_data["edit_message_id"],
#         reply_markup=keyboard_group_lineup_builder(state="enter_name"),
#     )
#     await state.set_state(GroupStates.update.enter_name)


# # -------------------group update_name update-----------------


# @teacher_user_router.message(
#     GroupStates.update.update_name,
#     (F.text.len() <= 10) & (F.text.len() >= 1),
#     flags=flags,
# )
# async def group_update_name_entering(
#     message: Message, state: FSMContext, bot: Bot
# ) -> None:
#     await state.update_data(name_upd=message.text.strip())
#     state_data = await state.get_data()
#     await message.delete()

#     def check_group_update_result_error(result: Union[None, str, Dict]) -> str:
#         errors = templates.UNTRACKED_ERROR_MESSAGE
#         if result and result != "Timeout":
#             errors = get_errors_from_dict(errors_dict=result)
#         return errors

#     result = await group_update_request(
#         upd_data={"name": state_data.get("name_upd")}, name=state_data.get("name")
#     )
#     errors_text = check_group_update_result_error(result)

#     await edit_message_text_safe(
#         bot=bot,
#         text=templates.GROUP_STUDENT_UPDATE_MESSAGE
#         if not result
#         else templates.ERROR_MESSAGE.format(errors=errors_text),
#         parse_mode=None,
#         chat_id=message.chat.id,
#         message_id=state_data["edit_message_id"],
#         reply_markup=keyboard_group_lineup_builder(state="add_student"),
#     )
#     if not result:
#         await state.set_state(GroupStates.add_student)
#     else:
#         await state.set_state(GroupStates.update.update_name)


# @teacher_user_router.message(
#     GroupStates.update.update_name,
#     flags=flags,
# )
# async def group_name_update_entering_failed(
#     message: Message, state: FSMContext, bot: Bot
# ) -> None:
#     state_data = await state.get_data()
#     await message.delete()
#     await edit_message_text_safe(
#         bot=bot,
#         text=templates.GROUP_NAME_FAILED_MESSAGE,
#         parse_mode=None,
#         chat_id=message.chat.id,
#         message_id=state_data["edit_message_id"],
#         reply_markup=keyboard_group_lineup_builder(state="enter_name"),
#     )
#     await state.set_state(GroupStates.update.update_name)


# -------------------group name enterance-----------------


@teacher_user_router.message(
    GroupStates.enter_name,
    (F.text.len() <= 10) & (F.text.len() >= 1),
    flags=flags,
)
async def group_name_entering(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(name=message.text.strip())
    state_data = await state.get_data()
    await message.delete()

    def check_group_list_result_error(
        result: Union[None, str, Dict], key: str = "detail"
    ) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = result.get(key, errors)
        return errors

    def check_group_result_error(result: Union[None, str, Dict]) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result and result != "Timeout":
            errors = get_errors_from_dict(errors_dict=result)
        return errors

    status_code, response = await student_all_list_request()

    data = [json.loads(json.dumps(obj)) for obj in response]

    formatted_strings = []

    for obj in data:
        email = obj["email"]
        name = obj["name"]
        last_name = obj["last_name"]
        surname = obj["surname"]
        group = obj["group"]

        formatted_string = (
            f"Емейл: {email}, ФІО: {name} {last_name} {surname}, Група: {group}"
        )

        formatted_strings.append(formatted_string)

    result_string = "\n".join(formatted_strings)

    result = await group_create_request(
        collected_data={
            "name": state_data.get("name"),
        }
    )

    errors_text = check_group_result_error(result)

    # text_result

    if status_code == 200:
        text_result = templates.GROUP_NAME_MESSAGE.format(result_string=result_string)
    elif not result:
        text_result = templates.GROUP_NAME_MESSAGE.format(result_string=result_string)
    elif status_code == 408:
        text_result = templates.ERROR_MESSAGE.format(
            errors=check_group_list_result_error(response)
        )
    else:
        text_result = templates.ERROR_MESSAGE.format(errors=errors_text)

    await edit_message_text_safe(
        bot=bot,
        text=text_result,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_group_lineup_builder(state="add_student"),
    )
    await state.set_state(GroupStates.add_student)


@teacher_user_router.message(
    GroupStates.enter_name,
    flags=flags,
)
async def group_name_entering_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.GROUP_NAME_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_group_lineup_builder(state="enter_name"),
    )
    await state.set_state(GroupStates.enter_name)


# -------------------group add student-----------------


@teacher_user_router.message(
    GroupStates.add_student,
    (F.text.len() <= 100) & (F.text.len() >= 1),
    EmailFilter(),
    flags=flags,
)
async def group_add_student(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(student=message.text.strip())
    state_data = await state.get_data()
    await message.delete()

    def check_group_result_error(
        result: Union[None, str, Dict], key: str = "detail"
    ) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result == "Timeout":
            errors = result.get(key, errors)
        return errors

    def check_register_result_error(result: Union[None, str, Dict]) -> str:
        errors = templates.UNTRACKED_ERROR_MESSAGE
        if result and result != "Timeout":
            errors = get_errors_from_dict(errors_dict=result)
        return errors

    status_code, response = await student_all_list_request()

    data = [json.loads(json.dumps(obj)) for obj in response]

    formatted_strings = []

    for obj in data:
        email = obj["email"]
        name = obj["name"]
        last_name = obj["last_name"]
        surname = obj["surname"]
        group = obj["group"]

        formatted_string = (
            f"Емейл: {email}, ФІО: {name} {last_name} {surname}, Група: {group}"
        )

        formatted_strings.append(formatted_string)

    result_string = "\n".join(formatted_strings)

    if state_data.get("name"):
        upd_data = state_data.get("name")
    else:
        upd_data = state_data.get("name_upd")

    result = await add_student_to_group(
        upd_data={"group": upd_data}, email=state_data.get("student")
    )

    errors_text = check_register_result_error(result)

    await edit_message_text_safe(
        bot=bot,
        text=templates.GROUP_ADD_STUDENT_MESSAGE.format(result_string=result_string)
        if status_code == 200
        else templates.ERROR_MESSAGE.format(errors=check_group_result_error(response)),
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_group_lineup_builder(state="add_student"),
    )
    await state.set_state(GroupStates.add_student)


@teacher_user_router.message(
    GroupStates.add_student,
    flags=flags,
)
async def group_add_student_failed(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    state_data = await state.get_data()
    await message.delete()
    await edit_message_text_safe(
        bot=bot,
        text=templates.GROUP_ADD_STUDENT_FAILED_MESSAGE,
        parse_mode=None,
        chat_id=message.chat.id,
        message_id=state_data["edit_message_id"],
        reply_markup=keyboard_group_lineup_builder(state="add_student"),
    )
    await state.set_state(GroupStates.enter_name)


# -------------------group end operation-----------------


@teacher_user_router.callback_query(
    GroupStates.add_student,
    Text(text=["End-account"]),
    flags=flags,
)
async def group_end_operation_callback_query(
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
        reply_markup=keyboard_group_lineup_builder(),
    )
    await state.clear()
