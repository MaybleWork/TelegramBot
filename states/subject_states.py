from aiogram.filters.state import State, StatesGroup


# class TestAnswerStates(StatesGroup):
#     enter_test_answer_text = State()
#     enter_test_answeris_correct = State()


# class MultitestStates(StatesGroup):
#     enter_multitest_answertext = State()
#     enter_multitestis_correct = State()
#     enter_multitestmark = State()


# class TestStates(StatesGroup):
#     enter_test_title = State()
#     enter_max_mark = State()
#     enter_number_of_attemps = State()
#     enter_visibility = State()
#     enter_automate_checking = State()
#     enter_question_randomizer = State()
#     enter_backstep = State()
#     enter_penalty = State()
#     enter_level = State()
#     enter_test_duration = State()
#     enter_start_date = State()
#     enter_end_date = State()
#     enter_count_of_question = State()
#     enter_subject = State()


# class QuestionStates(StatesGroup):
#     enter_question_text = State()
#     enter_question_mark = State()
#     enter_question_image = State()
#     enter_question_file = State()
#     enter_test = State()


class SubjectStudentStates(StatesGroup):
    enter_title = State()
    enter_test_title = State()
    send_answer = State()
    end_test = State()


class SubjectStates(StatesGroup):
    choose_keyboard = State()
    enter_subject_title = State()
    enter_group = State()
    enter_test_title = State()
    enter_max_mark = State()
    enter_number_of_attemps = State()
    enter_visibility = State()
    enter_automate_checking = State()
    enter_question_randomizer = State()
    enter_backstep = State()
    enter_penalty = State()
    enter_level = State()
    enter_test_duration = State()
    enter_start_date = State()
    enter_end_date = State()
    enter_count_of_question = State()
    enter_subject = State()
    enter_test_add_subject_tittle = State()
    enter_update_subject_title = State()
    enter_update_test_title = State()
    press_update_test_title = State()
    upd_max_mark = State()
    upd_number_of_attemps = State()
    upd_visibility = State()
    upd_automate_checking = State()
    upd_question_randomizer = State()
    upd_backstep = State()
    upd_penalty = State()
    upd_level = State()
    upd_test_duration = State()
    upd_start_date = State()
    upd_end_date = State()
    upd_count_of_question = State()
    enter_test_question_text = State()
    enter_question_text = State()
    enter_question_image = State()
    enter_question_file = State()
    enter_test = State()
    enter_test_mark = State()
    add_answer = State()
    enter_text_answer_mark = State()
    enter_test_answer_text = State()
    enter_test_answer_is_correct = State()
    enter_multitest_answer_text = State()
    enter_multitest_is_correct = State()
    enter_multitest_mark = State()
    enter_result = State()
    enter_answer = State()
    enter_mark = State()
    student = SubjectStudentStates
