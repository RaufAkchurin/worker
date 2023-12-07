import logging
import sys
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import test_kb
from keyboards import ObjectInlineKeyboard, ObjectCallbackFactory, CategoryInlineKeyboard, TypeInlineKeyboard, \
    CategoryCallbackFactory, TypeCallbackFactory
from workers_kb import WorkerInlineKeyboard, WorkerCallbackFactory
from states import Form
import os
from dotenv import load_dotenv

# TODO: Добавить проверку пользователя по ТГ-айди в БД
# TODO: Добавить проверку пароля
# TODO: Убрать все секретные данные в отдельный файл


# Загрузка переменных окружения из файла .env
load_dotenv()

BOT_LINK = "t.me/stroyka_worker_bot"
HELP_COMMAND = """
/help - список команд
/start - начать работу с ботом
"""

bot = Bot(os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.username
    await message.answer(f"Hello, AIOgram 3.x! Your user ID is {user_id}", reply_markup=test_kb.main_kb)


@dp.message()
async def echo(message: Message):
    msg = message.text.lower()

    if msg == "авторизоваться":
        await message.answer("Выберите своё имя:", reply_markup=WorkerInlineKeyboard())
    elif msg == "отпр. отчёт":
        await message.answer("Выберите объект на котором вы работали:", reply_markup=ObjectInlineKeyboard())
    elif msg == "назад":
        await message.answer("Вы перешли в главное меню!", reply_markup=test_kb.main_kb)


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
                             state: FSMContext
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
        text=f"Введите пожалуйста объём выполниненных работ в {callback_data.measurement}"
    )


@dp.callback_query(WorkerCallbackFactory.filter())
async def process_worker_name_press(callback: CallbackQuery,
                                    callback_data: WorkerCallbackFactory,
                                    state: FSMContext):
    await state.set_state(Form.password)
    await callback.message.answer(
        text=f'Айди рабочего: {callback_data.id}\n' \
             f'Выбрано имя: {callback_data.name}\n' \
             'Введите пожалуйста пароль',
    )


async def main() -> None:
    await bot.delete_webhook(
        drop_pending_updates=True)  # все команды при выключенном боте после включении его не будут обрабатываться
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
