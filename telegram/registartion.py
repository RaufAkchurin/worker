from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from django.telegram.API import get_worker_by_telegram, post_worker_registration


class RegisterState(StatesGroup):
    regName = State()
    regSurname = State()
    regPhone = State()
    confirmation = State()


async def register_start(message: Message, state: FSMContext):
    worker = get_worker_by_telegram(message.from_user.id)
    if worker:
        message_text = ('Вы зарегистрированы под следующими данными: \n' \
                             f'Имя: <u><b>{worker["worker"]["name"]}</b></u> \n' \
                             f'Фамилия: <u><b>{worker["worker"]["surname"]}</b></u> \n' \
                             f'Телефон: <u><b>{worker["worker"]["telephone"]}</b></u> \n' \
                             f'Телеграм_айди: <u><b>{message.from_user.id}</b></u> \n' \
                             )
        await message.answer(
            text=message_text,
            parse_mode=ParseMode.HTML,
        )
    else:
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
    data_from_state = await state.get_data()
    regname = data_from_state.get('regname')
    regsurname = data_from_state.get('regsurname')

    await message.answer(   f'Проверьте ваши данные: \n' \
                            f'Имя: {regname} \n' \
                            f'Фамилия: {regsurname} \n' \
                            f'Телефон: {message.text} \n' \
                            "Всё верно?(да/нет)")
    await state.update_data(regtelephone=message.text)
    await state.set_state(RegisterState.confirmation)


async def register_confirmation(message: Message, state: FSMContext):
    data_from_state = await state.get_data()
    name = data_from_state.get('regname')
    surname = data_from_state.get('regsurname')
    telephone = data_from_state.get('regtelephone')
    telegram_id = message.from_user.id

    if message.text == "да":
        response = post_worker_registration(name=name, surname=surname, telephone=telephone, telegram_id=telegram_id)
        if response:
            await message.answer('Регистрация прошла успешно 🆗\n' \
                                 'Теперь вы можете отправлять отчёты о работе с данного аккаунта телеграм 👷')
        else:
            await message.answer('⚠️Что то пошло не так, попробуйте снова, или обратитесь к разработчику⚠️')


        #TODO добавить логику отправки запроса на ендпоинт при 200 статусе
        #TODO добавить логику отправки запроса на ендпоинт при ошибках

    elif message.text == "нет":
        await state.set_state(RegisterState.regName)
        await message.answer("Введите ваше имя занова")
