from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    password = State()
