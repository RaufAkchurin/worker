import logging
import sys
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import test_kb
from django.telegram.API import get_worker_by_telegram
from django.telegram.registartion import RegisterState, register_start, register_name, register_phone, register_surname, \
    register_confirmation
from django.telegram.report import ReportState, report_value_input, report_confirmation
from keyboards import ObjectInlineKeyboard, ObjectCallbackFactory, CategoryInlineKeyboard, TypeInlineKeyboard, \
    CategoryCallbackFactory, TypeCallbackFactory
from workers_kb import WorkerInlineKeyboard
import os
from dotenv import load_dotenv

load_dotenv()

HELP_COMMAND = """
/help - список команд
/start - начать работу с ботом
"""

bot = Bot(os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher()

# Регистрируем хендлеры регистрации нового пользователя
dp.message.register(register_start, F.text == 'Регистрация/Профиль')
dp.message.register(register_name, RegisterState.regName)
dp.message.register(register_surname, RegisterState.regSurname)
dp.message.register(register_phone, RegisterState.regPhone)
dp.message.register(register_confirmation, RegisterState.confirmation)

# Регистрируем хендлеры отчётов
dp.message.register(report_value_input, ReportState.value)
dp.message.register(report_confirmation, ReportState.confirmation)


@dp.message(CommandStart())
async def start(message: Message):
    if get_worker_by_telegram(message.from_user.id):
        await message.answer(f"Привет, бот запустился", reply_markup=test_kb.main_kb)
    else:
        await message.answer("Пожалуйста пройдите регистрацию.", reply_markup=test_kb.main_kb)


@dp.message()
async def echo(message: Message):
    msg = message.text.lower()
    if msg == "авторизоваться":
        await message.answer("Выберите своё имя:", reply_markup=WorkerInlineKeyboard())
    elif msg == "отправить отчёт":
        # TODO добавить проверку на наличие телеграм айди
        if get_worker_by_telegram(message.from_user.id):
            await message.answer("Выберите объект на котором вы работали:", reply_markup=ObjectInlineKeyboard())
        else:
            await message.answer("⚠️ Вы не можете отправлять отчёты, вам необходимо пройти регистрацию. ⚠️")
    elif msg == "перезагрузить бота":
        await message.answer("Вы перешли в главное меню!", reply_markup=test_kb.main_kb)


@dp.callback_query(ObjectCallbackFactory.filter())
async def process_object_press(callback: CallbackQuery,
                               callback_data: ObjectCallbackFactory,
                               state: FSMContext):
    await state.update_data(selected_object_name=callback_data.name)
    await callback.message.answer(
        text=f'Название объекта: {callback_data.name}\n',
        reply_markup=CategoryInlineKeyboard(callback_data.id)
    )


@dp.callback_query(CategoryCallbackFactory.filter())
async def process_category_press(callback: CallbackQuery,
                                 callback_data: CategoryCallbackFactory,
                                 state: FSMContext):
    await state.update_data(selected_category_id=callback_data.id)
    await state.update_data(selected_category_name=callback_data.name)
    await callback.message.answer(
        text=f'Название категории: {callback_data.name}\n',
        reply_markup=TypeInlineKeyboard(callback_data.id)
    )


@dp.callback_query(TypeCallbackFactory.filter())
async def process_type_press(callback: CallbackQuery,
                             callback_data: TypeCallbackFactory,
                             state: FSMContext,
                             ):

    await state.update_data(selected_type_id=callback_data.id)  # Для пост запроса на создание смены
    await state.update_data(selected_type_name=callback_data.name)
    await state.update_data(selected_type_measurement=callback_data.measurement)

    message_text = (f'Тип работ: {callback_data.name} \n' \
                    f'                                              \n' \
                    f"Введите пожалуйста объём выполниненных работ в <u><b>{callback_data.measurement}</b></u>\n"
                    )
    await callback.message.answer(
        text=message_text,
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(ReportState.value)


async def main() -> None:
    await bot.delete_webhook(
        drop_pending_updates=True)  # все команды при выключенном боте после включении его не будут обрабатываться
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
