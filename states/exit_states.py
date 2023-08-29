from aiogram.filters.state import State, StatesGroup


class LogoutStates(StatesGroup):
    logout = State()
