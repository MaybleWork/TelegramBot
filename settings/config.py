from typing import List, Any
from .db import BotDB
from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    # bot_owner: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class APIEndpoints(BaseSettings):
    api_schema: str
    student_registration_post: str
    student_all_list: str
    student_add_patch: str
    student_group_get: str
    student_get: str
    teacher_registration_post: str
    teacher_id_get: str
    user_auth: str
    user_update: str
    group_create_post: str
    group_all_list: str
    group_update: str
    subject_teacherlist_get: str
    subject_studentlist_get: str
    subject_create_post: str
    subject_title_get: str
    test_create_post: str
    test_visiblelist_get: str
    test_student_get: str
    test_subject_list_get: str
    test_title_patch: str
    question_create_post: str
    question_list_get: str
    answer_create_post: str
    answer_list_get: str
    answer_text_get: str
    answer_question_get: str
    result_create_post: str
    result_update_patch: str
    result_name_get: str
    result_decrise_patch: str
    result_student_list_get: str
    result_teacher_list_get: str
    verif_code_get: str

    class Config:
        env_file = ".api-endpoints.env"
        env_file_encoding = "utf-8"


config = Settings()
api_endpoints = APIEndpoints()
bot_db = BotDB("bot.db")
