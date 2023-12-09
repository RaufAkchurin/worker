import logging
import sys
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import test_kb
from django.telegram.API import get_worker_by_telegram
from django.telegram.register import RegisterState
from keyboards import ObjectInlineKeyboard, ObjectCallbackFactory, CategoryInlineKeyboard, TypeInlineKeyboard, \
    CategoryCallbackFactory, TypeCallbackFactory
from workers_kb import WorkerInlineKeyboard, WorkerCallbackFactory
from states import Form
import os
from dotenv import load_dotenv

# TODO: Добавить проверку пользователя по ТГ-айди в БД
# TODO: Добавить проверку пароля
load_dotenv()

HELP_COMMAND = """
/help - список команд
/start - начать работу с ботом
"""

bot = Bot(os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher()


async def start_register(message: Message, state: FSMContext):
    await message.answer(f'⭐ Давайте начнём регистрацию \n Для начала скажите, как к вас зовут? ⭐')
    await state.set_state(RegisterState.regName)


async def register_name(message: Message, state: FSMContext):
    await message.answer(f'Приятно познакомиться {message.text} \n'
                         f'Теперь укажите номер телефона, чтобы быть на связи \n'
                         f'Формат телефона: +7xxxxxxxx \n\n'
                         )
    await state.update_data(regname=message.text)
    await state.set_state(RegisterState.regPhone)


# обрабатываем ввод телефона
async def register_phone(message: Message, state: FSMContext):
    await message.answer("Спасибо за телефон")
    await state.update_data(regphone=message.text)
    await state.clear()


# Регистрируем хендлеры регистрации
dp.message.register(start_register, F.text == 'Пройти регистрацию')
dp.message.register(register_name, RegisterState.regName)
dp.message.register(register_phone, RegisterState.regPhone)


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    id = message.from_user.id

    if get_worker_by_telegram(message.from_user.id):
        await state.update_data(user_registered=True)
        await message.answer(f"Привет, твой айди - {id}", reply_markup=test_kb.main_kb_for_registered)
    else:
        await state.update_data(user_registered=False)
        await message.answer("Пожалуйста пройдите регистрацию.", reply_markup=test_kb.main_kb_for_unregistered)


@dp.message()
async def echo(message: Message):
    msg = message.text.lower()

    if msg == "авторизоваться":
        await message.answer("Выберите своё имя:", reply_markup=WorkerInlineKeyboard())
    elif msg == "отпр. отчёт":
        await message.answer("Выберите объект на котором вы работали:", reply_markup=ObjectInlineKeyboard())
    elif msg == "назад":
        await message.answer("Вы перешли в главное меню!", reply_markup=test_kb.main_kb_for_registered)


@dp.callback_query(ObjectCallbackFactory.filter())
async def process_object_press(callback: CallbackQuery,
                               callback_data: ObjectCallbackFactory,
                               state: FSMContext):
    await state.update_data(selected_object_name=callback_data.name)
    await callback.message.answer(
        text=f'Айди объекта: {callback_data.id}\n' \
             f'Название объекта: {callback_data.name}\n',
        reply_markup=CategoryInlineKeyboard(callback_data.id)
    )


@dp.callback_query(CategoryCallbackFactory.filter())
async def process_category_press(callback: CallbackQuery,
                                 callback_data: CategoryCallbackFactory,
                                 state: FSMContext):
    await state.update_data(selected_category_id=callback_data.id)
    await state.update_data(selected_category_name=callback_data.name)
    await callback.message.answer(
        text=f'Айди категории: {callback_data.id}\n' \
             f'Название категории: {callback_data.name}\n',
        reply_markup=TypeInlineKeyboard(callback_data.id)
    )


@dp.callback_query(TypeCallbackFactory.filter())
async def process_type_press(callback: CallbackQuery,
                             callback_data: TypeCallbackFactory,
                             state: FSMContext,
                             ):
    data = await state.get_data()
    selected_type_name = data.get('selected_category_name')
    selected_object_name = data.get('selected_object_name')

    await callback.message.answer(
        text=f'Объект: {selected_object_name}\n' \
             f'Категория: {selected_type_name}\n' \
             f'Тип работ: {callback_data.name}\n' \
             f'тип изм.: {callback_data.measurement}\n',
        # reply_markup=TypeInlineKeyboard(callback_data.id)
    )
    await callback.message.answer(
        text=f"Введите пожалуйста объём выполниненных работ в {callback_data.measurement}\n" \
             f"Ваш айди {callback.from_user.id}"
    )


@dp.callback_query(WorkerCallbackFactory.filter())
async def process_worker_name_press(callback: CallbackQuery,
                                    callback_data: WorkerCallbackFactory,
                                    state: FSMContext):
    await state.set_state(Form.password)
    await callback.message.answer(
        text=f'Выбрано имя: {callback_data.name}\n' \
             'Введите пожалуйста пароль',
    )


async def main() -> None:
    await bot.delete_webhook(
        drop_pending_updates=True)  # все команды при выключенном боте после включении его не будут обрабатываться
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
