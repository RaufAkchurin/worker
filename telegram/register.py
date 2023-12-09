from aiogram.fsm.state import StatesGroup, State


class RegisterState(StatesGroup):
    regName = State()
    regSurname = State()
    regPhone = State()

