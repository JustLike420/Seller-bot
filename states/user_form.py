from aiogram.dispatcher.filters.state import StatesGroup, State


class UserForm(StatesGroup):
    choice = State()
    name = State()
    phone = State()
    email = State()
