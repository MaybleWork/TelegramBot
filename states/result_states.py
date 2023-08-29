from aiogram.filters.state import State, StatesGroup


class ResultStates(StatesGroup):
    choose_keyboard = State()
    get_result = State()
