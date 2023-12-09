from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message


class RegisterState(StatesGroup):
    regName = State()
    regSurname = State()
    regPhone = State()
    confirmation = State()


async def register_start(message: Message, state: FSMContext):
    await message.answer(f'⭐ Давайте начнём регистрацию \n Для начала скажите, как к вас зовут? ⭐')
    await state.set_state(RegisterState.regName)


async def register_name(message: Message, state: FSMContext):
    #TODO добавить валидацию чтобы были только буквы, и чтобы не слишком длинно было
    await message.answer(f'Приятно познакомиться {message.text} \n'
                         f"Введите вашу фамилию"
                         )
    await state.update_data(regname=message.text)
    await state.set_state(RegisterState.regSurname)


async def register_surname(message: Message, state: FSMContext):
    # TODO добавить валидацию чтобы были только буквы, и чтобы не слишком длинно было
    await message.answer(f'Ваша фамилия {message.text} \n'
                         f'Теперь укажите номер телефона, чтобы быть на связи \n'
                         )
    await state.update_data(regsurname=message.text)
    await state.set_state(RegisterState.regPhone)


async def register_phone(message: Message, state: FSMContext):
    # TODO добавить валидацию
    data = await state.get_data()
    regname = data.get('regname')
    regsurname = data.get('regsurname')

    await message.answer(   f'Проверьте ваши данные: \n' \
                            f'Имя: {regname} \n' \
                            f'Фамилия: {regsurname} \n' \
                            f'Телефон: {message.text} \n' \
                            "Всё верно?(да/нет)")
    await state.update_data(regphone=message.text)
    await state.set_state(RegisterState.confirmation)


async def register_confirmation(message: Message, state: FSMContext):
    if message.text == "да":
        await message.answer('Регистрация прошла успешно 🆗\n' \
                            'Теперь вы можете отправлять отчёты о работе с данного аккаунта телеграм 👷')
        #TODO добавить логику отправки запроса на ендпоинт при 200 статусе
        #TODO добавить логику отправки запроса на ендпоинт при ошибках

    elif message.text == "нет":
        await state.set_state(RegisterState.regName)
        await message.answer("Введите ваше имя занова")
