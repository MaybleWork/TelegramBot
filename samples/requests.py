import aiohttp
import logging
import asyncio

from settings.config import config, api_endpoints


async def verif_code_request(verification_code: str):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
        ) as session:
            async with session.get(
                api_endpoints.verif_code_get.format(code=verification_code),
            ) as response:
                if response.status == 200:
                    return None
                return await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return "Timeout"


async def student_reg_request(collected_data: dict):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.post(
                api_endpoints.student_registration_post,
                data=collected_data,
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                if response.status == 201:
                    return None
                return await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return "Timeout"


async def student_group_request(email: str):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.get(
                api_endpoints.student_group_get.format(email=email),
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                return response.status, await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return 408, "Timeout"


async def student_all_list_request():
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.get(
                api_endpoints.student_all_list,
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                return response.status, await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return 408, "Timeout"


async def student_get_request(email: str):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.get(
                api_endpoints.student_get.format(email=email),
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                return response.status, await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return 408, "Timeout"


async def teacher_reg_request(collected_data: dict):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.post(
                api_endpoints.teacher_registration_post,
                data=collected_data,
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                if response.status == 201:
                    return None
                return await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return "Timeout"


async def teacher_pk_request(email: str):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.get(
                api_endpoints.teacher_id_get.format(email=email),
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                return response.status, await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return 408, "Timeout"


async def subject_create_request(collected_data: dict):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.post(
                api_endpoints.subject_create_post,
                data=collected_data,
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                if response.status == 201:
                    return None
                return await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return "Timeout"


async def subject_title_request(title: str):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.get(
                api_endpoints.student_group_get.format(title=title),
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                return response.status, await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return 408, "Timeout"


async def subject_teacherlist_request(fk: str):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.get(
                api_endpoints.subject_teacherlist_get.format(fk=fk),
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                return response.status, await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return 408, "Timeout"


async def subject_studentlist_request(name: str):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.get(
                api_endpoints.subject_studentlist_get.format(name=name),
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                return response.status, await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return 408, "Timeout"


async def test_student_list_request(title: str):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.get(
                api_endpoints.test_visiblelist_get.format(subject=title),
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                return response.status, await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return 408, "Timeout"


async def test_subject_list_request(subject: str):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.get(
                api_endpoints.test_subject_list_get.format(subject=subject),
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                return response.status, await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return 408, "Timeout"


async def test_creation_request(collected_data: dict):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.post(
                api_endpoints.test_create_post,
                data=collected_data,
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                if response.status == 201:
                    return None
                return await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return "Timeout"


async def test_student_get_request(title: str):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.get(
                api_endpoints.test_student_get.format(title=title),
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                return response.status, await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return 408, "Timeout"


async def updating_test(upd_data: dict, title: str):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.patch(
                api_endpoints.test_title_patch.format(title=title),
                data=upd_data,
                timeout=30,
            ) as response:
                logging.info(f"Login response status: {response.status}")
                return response.status, await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return 408, "Timeout"


async def question_creation_request(collected_data: dict):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.post(
                api_endpoints.question_create_post,
                data=collected_data,
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                if response.status == 201:
                    return None
                return await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return "Timeout"


async def question_list_request(title: str, page=None):
    params = {"page": page}
    params = dict(filter(lambda item: item[1] is not None, params.items()))

    async with aiohttp.ClientSession(
        api_endpoints.api_schema,
    ) as session:
        async with session.get(
            api_endpoints.question_list_get.format(title=title), params=params
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None


async def answer_creation_request(collected_data: dict):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.post(
                api_endpoints.answer_create_post,
                data=collected_data,
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                return response.status, response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return 404, "Timeout"


async def answert_list_request(text: str):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.get(
                api_endpoints.answer_list_get.format(text=text),
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                return response.status, await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return 408, "Timeout"


async def answert_get_request(text: str):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.get(
                api_endpoints.answer_text_get.format(text=text),
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                return response.status, await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return 408, "Timeout"


async def answert_question_get_request(question: str):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.get(
                api_endpoints.answer_question_get.format(question=question),
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                return response.status, await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return 408, "Timeout"


async def result_creation_request(collected_data: dict):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.post(
                api_endpoints.result_create_post,
                data=collected_data,
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                if response.status == 201:
                    return None
                return await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return "Timeout"


async def result_get_request(name: str):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.get(
                api_endpoints.result_name_get.format(name=name),
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                return response.status, await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return 408, "Timeout"


async def updating_result(upd_data: dict, name: str):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.patch(
                api_endpoints.result_update_patch.format(name=name),
                data=upd_data,
                timeout=30,
            ) as response:
                logging.info(f"Login response status: {response.status}")
                return response.status, await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return 408, "Timeout"


async def result_decrise(name: str, title: str):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.patch(
                api_endpoints.result_decrise_patch.format(name=name, title=title),
                timeout=30,
            ) as response:
                logging.info(f"Login response status: {response.status}")
                if response.status == 200:
                    return None
                else:
                    await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return 408, "Timeout"


async def result_student_list_request(fk: int):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.get(
                api_endpoints.result_student_list_get.format(fk=fk),
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                return response.status, await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return 408, "Timeout"


async def result_teacher_list_request(title: int):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.get(
                api_endpoints.result_teacher_list_get.format(title=title),
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                return response.status, await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return 408, "Timeout"


async def authorization_user(auth_data: dict):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.post(
                api_endpoints.user_auth,
                data=auth_data,
                timeout=30,
            ) as response:
                logging.info(f"Login response status: {response.status}")
                return response.status, await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return 408, "Timeout"


async def updating_user(upd_data: dict, email: str):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.patch(
                api_endpoints.user_update.format(email=email),
                data=upd_data,
                timeout=30,
            ) as response:
                logging.info(f"Login response status: {response.status}")
                return response.status, await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return 408, "Timeout"


async def group_create_request(collected_data: dict):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.post(
                api_endpoints.group_create_post,
                data=collected_data,
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                if response.status == 201:
                    return None
                return await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return "Timeout"


async def add_student_to_group(upd_data: dict, email: str):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.patch(
                api_endpoints.student_add_patch.format(email=email),
                data=upd_data,
                timeout=30,
            ) as response:
                logging.info(f"Login response status: {response.status}")
                if response.status == 200:
                    return None
                return await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return "Timeout"


async def group_all_list_request():
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.get(
                api_endpoints.group_all_list,
                timeout=30,
            ) as response:
                logging.info(f"Registration response status: {response.status}")
                return response.status, await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return 408, "Timeout"


async def group_update_request(upd_data: dict, name: str):
    try:
        async with aiohttp.ClientSession(
            api_endpoints.api_schema,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as session:
            async with session.patch(
                api_endpoints.group_update.format(name=name),
                json=upd_data,
                timeout=30,
            ) as response:
                logging.info(f"Login response status: {response.status}")
                if response.status == 200:
                    return None
                return await response.json()
    except asyncio.TimeoutError:
        logging.error("Request to API timed out")
        return "Timeout"
