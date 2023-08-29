from aiogram.filters.state import State, StatesGroup


class RegistrationStudent(StatesGroup):
    enter_email_login = State()
    enter_name = State()
    enter_last_name = State()
    enter_surname = State()
    enter_password = State()
    start_auth = State()


class RegistrationTeacher(StatesGroup):
    enter_email_login = State()
    enter_name = State()
    enter_last_name = State()
    enter_surname = State()
    enter_password = State()
    enter_verif_code = State()
    start_auth = State()


class Authorization(StatesGroup):
    enter_email_login = State()
    enter_password = State()


class UserRegistrationStates(StatesGroup):
    choose_keyboard = State()
    auth = Authorization
    reg_teacher = RegistrationTeacher
    reg_student = RegistrationStudent
