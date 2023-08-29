from aiogram.filters.state import State, StatesGroup


class AccountUpdateStates(StatesGroup):
    choose_kb = State()
    update_email = State()
    update_name = State()
    update_last_name = State()
    update_surname = State()
