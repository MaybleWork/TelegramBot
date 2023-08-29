from aiogram.filters.state import State, StatesGroup


class GrroupUpdateStates(StatesGroup):
    enter_name = State()
    update_name = State()


class GroupStates(StatesGroup):
    choose_keyboard = State()
    add_student = State()
    enter_name = State()
    update = GrroupUpdateStates
