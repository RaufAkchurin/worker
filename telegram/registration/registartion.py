from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from telegram.API import get_worker_by_telegram, post_worker_registration


class RegisterState(StatesGroup):
    regName = State()
    regSurname = State()
    regPhone = State()
    confirmation = State()


async def answer_for_registered_user(message: Message, worker, bot: Bot):
    message_text = ('👷 Вы зарегистрированы под следующими данными: \n' \
                    f'Имя: <u><b>{worker["worker"]["name"]}</b></u> \n' \
                    f'Фамилия: <u><b>{worker["worker"]["surname"]}</b></u> \n' \
                    f'Телефон: <u><b>{worker["worker"]["telephone"]}</b></u> \n' \
                    f'Телеграм_айди: <u><b>{message.from_user.id}</b></u> \n' \
                    )
    await bot.send_message(
        message.from_user.id,
        text=message_text,
        parse_mode=ParseMode.HTML,
    )


async def register_start(message: Message, state: FSMContext, bot: Bot):
    worker = get_worker_by_telegram(message.from_user.id)
    if worker:
        await answer_for_registered_user(message=message, worker=worker, bot=bot)
    else:
        await bot.send_message(message.from_user.id,
                               text=f'📝 Давайте начнём регистрацию \n Для начала скажите, как к вас зовут? 📝')
        await state.set_state(RegisterState.regName)


async def register_name(message: Message, state: FSMContext, bot: Bot):
    if message.text.isalpha() and len(message.text) <= 12:
        await state.update_data(regname=message.text)
        await state.set_state(RegisterState.regSurname)
        await bot.send_message(message.from_user.id, text=f'🤝 Приятно познакомиться {message.text.capitalize()} 🤝\n '
                                                          f"Введите пожалуйста вашу фамилию"
                               )
    else:
        await bot.send_message(message.from_user.id,
                               text="⚠️Имя должно содержать только буквы, и длина не должна превышать 12 символов⚠️")


async def register_surname(message: Message, state: FSMContext, bot: Bot):
    if message.text.isalpha() and len(message.text) <= 12:
        await bot.send_message(message.from_user.id, text=f'⭐ Ваша фамилия {message.text.capitalize()}⭐ \n '
                                                          f'📱 Теперь укажите номер телефона, который доступен для связи.\n'
                                                          f'                                                             \n'
                                                          f'⚠️ Формат телефона: 89172839062\n'
                               )
        await state.update_data(regsurname=message.text)
        await state.set_state(RegisterState.regPhone)
    else:
        await bot.send_message(message.from_user.id,
                               text="⚠️ Фамилия должна содержать только буквы, и длина не должна превышать 12 символов⚠️")


async def register_phone(message: Message, state: FSMContext, bot: Bot):
    # TODO добавить валидацию
    data_from_state = await state.get_data()
    regname = data_from_state.get('regname')
    regsurname = data_from_state.get('regsurname')

    if message.text.isdigit() and len(message.text) == 11:
        await bot.send_message(message.from_user.id, text=f'Проверьте ваши данные: \n' \
                                                          f'Имя: {regname} \n' \
                                                          f'Фамилия: {regsurname} \n' \
                                                          f'Телефон: {message.text} \n' \
                                                          "Всё верно?(да/нет)")
        await state.update_data(regtelephone=message.text)
        await state.set_state(RegisterState.confirmation)
    else:
        await bot.send_message(message.from_user.id, text="⚠️Номер указан в неправильном формате⚠️")


async def register_confirmation(message: Message, state: FSMContext, bot: Bot):
    data_from_state = await state.get_data()
    name = data_from_state.get('regname')
    surname = data_from_state.get('regsurname')
    telephone = data_from_state.get('regtelephone')
    telegram_id = message.from_user.id

    if message.text == "да":
        response = post_worker_registration(name=name, surname=surname, telephone=telephone, telegram_id=telegram_id)
        if response:
            await bot.send_message(message.from_user.id, text='Регистрация прошла успешно 🆗\n' \
                                                              'Теперь вы можете отправлять отчёты о работе с данного аккаунта телеграм 👷')
            await state.clear()  # Очищаем стейт только если прошло положительно иначе - чтобы запускалось занова
        else:
            await bot.send_message(message.from_user.id,
                                   text='⚠️Что то пошло не так, попробуйте снова, или обратитесь к разработчику⚠️')

    elif message.text == "нет":
        await state.clear()
        await state.set_state(RegisterState.regName)
        await bot.send_message(message.from_user.id, text="Введите ваше имя занова")

    else:
        await bot.send_message(message.from_user.id, text="⚠️ Ответить можно только да или нет⚠️")
